#include <WiFi.h>
#include <PubSubClient.h>
#include <ESP32Servo.h>
#include <HX711.h>
#include <WiFiUdp.h>
#include <NTPClient.h>
#include <ArduinoJson.h>   // Para parsear JSON

/*************** CONFIGURACIÓN WIFI ***************/
const char* ssid     = "Pablo_iPhone";
const char* password = "datos123";

/*************** CONFIGURACIÓN MQTT ***************/
const char* mqttServer = "broker.hivemq.com";
const int   mqttPort   = 1883;
const char* topicschedule  = "IoT/testESP32/sub";   // aquí recibimos JSON de horarios
const char* topicEvento    = "IoT/testESP32/pub";   // aquí publicamos estado

WiFiClient espClient;
PubSubClient mqttClient(espClient);

/*************** NTP ***************/
WiFiUDP ntpUDP;
// México centro (CDMX / Jalisco) UTC-6 (ajusta si hace falta)
NTPClient timeClient(ntpUDP, "pool.ntp.org", -21600);

/*************** PINS ***************/
#define SERVO_PIN   13
#define SERVO2_PIN  12
#define TRIG_PIN    14
#define ECHO_PIN    16
#define LED_PIN     23

Servo myServo;   // superior
Servo myServo2;  // inferior (invertido)

/*************** BALANZA ***************/
HX711 balanza;
const int HX_DOUT = 32;
const int HX_SCK  = 33;

long  lecturaCero        = 0;
float factorCalibracion  = 94.5;
float porcionDefecto     = 400.0;
const float ALTURA_CONTENEDOR = 25.0;
const float UMBRAL_BAJO       = 4.0;

/*************** HORARIOS DESDE JSON ***************/
struct Horario {
  int   hora;
  int   minuto;
  float porcion;
  bool  ejecutado;
  bool  preAvisado;    // aviso 5 min antes
  bool  postAvisado;   // aviso 5 min después
};

const int MAX_HORARIOS = 20;
Horario   horarios[MAX_HORARIOS];
int       cantidadHorarios = 0;

int lastHourChecked   = -1;
int lastMinuteChecked = -1;
unsigned long lastNtpUpdateMs = 0;

/*************** FUNCIONES ***************/

void reconnectMQTT() {
  while (!mqttClient.connected()) {
    Serial.print("MQTT conectando... ");
    if (mqttClient.connect("ComederoESP32")) {
      Serial.println("Conectado a MQTT");
      mqttClient.subscribe(topicschedule);
    } else {
      Serial.print("Error MQTT: ");
      Serial.println(mqttClient.state());
      delay(2000);
    }
  }
}

long medirDistancia() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duracion = pulseIn(ECHO_PIN, HIGH, 30000);
  if (duracion == 0) return -1;

  float distancia = duracion * 0.034 / 2.0;
  if (distancia > 200) return -1;
  return distancia;
}

float leerPeso() {
  long lecturaActual = balanza.read_average(40);
  long diferencia    = lecturaActual - lecturaCero;
  float peso         = -diferencia / factorCalibracion;
  return peso;
}

/************** SERVIR COMIDA **************/
void servirPorHorario(int indiceHorario) {
  float porcionObjetivo = horarios[indiceHorario].porcion;
  if (porcionObjetivo <= 0) porcionObjetivo = porcionDefecto;

  Serial.print("🍽 Iniciando servicio horario ");
  Serial.print(horarios[indiceHorario].hora);
  Serial.print(":");
  Serial.println(horarios[indiceHorario].minuto);

  // Abrir servos según tu montaje
  myServo.write(60);       // servo superior abre
  myServo2.write(120);     // servo inferior abre invertido
  delay(300);

  unsigned long inicioServicio = millis();
  const unsigned long timeoutMs = 60000;

  while (true) {
    mqttClient.loop();  // mantener conexión MQTT viva

    float pesoActual = leerPeso();
    Serial.print("⚖ Peso: ");
    Serial.println(pesoActual);

    if (pesoActual >= (porcionObjetivo - 30)) {
      Serial.println("✅ Porción alcanzada");
      break;
    }

    if (millis() - inicioServicio > timeoutMs) {
      Serial.println("⏱ Timeout sirviendo");
      break;
    }

    delay(500);
  }

  // Cerrar servos según tu montaje
  myServo.write(10);        // cerrar superior
  myServo2.write(170);     // cerrar inferior invertido
  delay(300);

  // Lecturas de sensores DESPUÉS de servir
  long distanciaHastaComida = medirDistancia();
  float distanciaAlimento = -1.0;

  if (distanciaHastaComida >= 0) {
    distanciaAlimento = (float)distanciaHastaComida;

    float nivelComida = ALTURA_CONTENEDOR - distanciaAlimento;
    nivelComida = constrain(nivelComida, 0, ALTURA_CONTENEDOR);

    if (nivelComida <= UMBRAL_BAJO) {
      digitalWrite(LED_PIN, HIGH);
    } else {
      digitalWrite(LED_PIN, LOW);
    }
  }

  float pesoFinal = leerPeso();

  // Hora real del evento
  timeClient.update();
  int h = timeClient.getHours();
  int m = timeClient.getMinutes();
  int s = timeClient.getSeconds();

  char horaRealStr[9];
  snprintf(horaRealStr, sizeof(horaRealStr), "%02d:%02d:%02d", h, m, s);

  // Horario programado
  char horarioStr[9];
  snprintf(horarioStr, sizeof(horarioStr), "%02d:%02d:%02d",
           horarios[indiceHorario].hora,
           horarios[indiceHorario].minuto,
           0);

  // JSON del evento principal ("servicio")
  char buffer[300];
  snprintf(buffer, sizeof(buffer),
           "{\"hora\":\"%s\",\"horario\":\"%s\",\"tipo\":\"servicio\",\"sensores\":["
             "{\"id\":1,\"valor\":%.2f,\"unidad\":\"cm\"},"
             "{\"id\":2,\"valor\":%.2f,\"unidad\":\"g\"}"
           "]}",
           horaRealStr,
           horarioStr,
           distanciaAlimento,
           pesoFinal);

  if (!mqttClient.connected()) reconnectMQTT();

  mqttClient.publish(topicEvento, buffer);
  Serial.println("📤 Publicado (servicio):");
  Serial.println(buffer);

  horarios[indiceHorario].ejecutado = true;
  Serial.println("Ejecutado ✔");
}

/************** AVISOS PRE / POST (CON SENSORES) **************/
void enviarAvisoHorario(int indiceHorario, const char* tipoEvento) {
  // tipoEvento: "pre" o "post"

  // Leer sensores en el momento del aviso
  long distanciaHastaComida = medirDistancia();
  float distanciaAlimento = -1.0;

  if (distanciaHastaComida >= 0) {
    distanciaAlimento = (float)distanciaHastaComida;

    float nivelComida = ALTURA_CONTENEDOR - distanciaAlimento;
    nivelComida = constrain(nivelComida, 0, ALTURA_CONTENEDOR);

    if (nivelComida <= UMBRAL_BAJO) {
      digitalWrite(LED_PIN, HIGH);
    } else {
      digitalWrite(LED_PIN, LOW);
    }
  }

  float pesoActual = leerPeso();

  // Hora real del aviso
  timeClient.update();
  int h = timeClient.getHours();
  int m = timeClient.getMinutes();
  int s = timeClient.getSeconds();

  char horaRealStr[9];
  snprintf(horaRealStr, sizeof(horaRealStr), "%02d:%02d:%02d", h, m, s);

  // Horario programado
  char horarioStr[9];
  snprintf(horarioStr, sizeof(horarioStr), "%02d:%02d:%02d",
           horarios[indiceHorario].hora,
           horarios[indiceHorario].minuto,
           0);

  // JSON de aviso "pre"/"post" con sensores
  char buffer[300];
  snprintf(buffer, sizeof(buffer),
           "{\"hora\":\"%s\",\"horario\":\"%s\",\"tipo\":\"%s\",\"sensores\":["
             "{\"id\":1,\"valor\":%.2f,\"unidad\":\"cm\"},"
             "{\"id\":2,\"valor\":%.2f,\"unidad\":\"g\"}"
           "]}",
           horaRealStr,
           horarioStr,
           tipoEvento,
           distanciaAlimento,
           pesoActual);

  if (!mqttClient.connected()) reconnectMQTT();

  mqttClient.publish(topicEvento, buffer);
  Serial.print("📤 Aviso ");
  Serial.print(tipoEvento);
  Serial.println(" enviado:");
  Serial.println(buffer);
}

/************** JSON DE HORARIOS **************/
void procesarJSONHorarios(const String& json) {
  Serial.println("🧩 Procesando JSON:");
  Serial.println(json);

  StaticJsonDocument<2048> doc;
  DeserializationError error = deserializeJson(doc, json);
  if (error) {
    Serial.print("❌ Error parseando JSON: ");
    Serial.println(error.c_str());
    return;
  }

  if (!doc.containsKey("horarios")) {
    Serial.println("❌ JSON sin 'horarios'");
    return;
  }

  JsonArray arr = doc["horarios"].as<JsonArray>();
  int n = arr.size();
  if (n > MAX_HORARIOS) n = MAX_HORARIOS;

  cantidadHorarios = n;

  for (int i = 0; i < n; i++) {
    JsonObject item = arr[i];

    const char* horaStr = item["hora"] | "00:00:00";
    int hh=0, mm=0, ss=0;

    int num = sscanf(horaStr, "%d:%d:%d", &hh, &mm, &ss);
    if (num < 2) {
      Serial.print("❌ Hora inválida en índice ");
      Serial.print(i);
      Serial.print(" -> ");
      Serial.println(horaStr);
      hh = 0; mm = 0;
    }

    horarios[i].hora      = hh;
    horarios[i].minuto    = mm;
    horarios[i].porcion   = item["porcion"] | porcionDefecto;
    horarios[i].ejecutado = false;
    horarios[i].preAvisado  = false;
    horarios[i].postAvisado = false;

    Serial.print("✔ Cargado horario ");
    Serial.print(hh); Serial.print(":"); Serial.println(mm);
  }

  Serial.print("Total horarios: ");
  Serial.println(cantidadHorarios);
}

/************** CALLBACK MQTT **************/
void mqttCallback(char* topic, byte* payload, unsigned int length) {
  String msg;
  for (unsigned int i = 0; i < length; i++) msg += (char)payload[i];

  Serial.print("📩 MQTT ");
  Serial.print(topic);
  Serial.print(": ");
  Serial.println(msg);

  if (String(topic) == String(topicschedule)) {
    procesarJSONHorarios(msg);
  }
}

/************** REVISAR HORARIOS **************/
void revisarHorarios() {
  unsigned long nowMs = millis();
  if (nowMs - lastNtpUpdateMs < 5000) return;  // cada 5 s
  lastNtpUpdateMs = nowMs;

  timeClient.update();
  time_t now = timeClient.getEpochTime();
  struct tm* timeinfo = localtime(&now);

  int h = timeinfo->tm_hour;
  int m = timeinfo->tm_min;

  if (h == lastHourChecked && m == lastMinuteChecked) return;

  lastHourChecked   = h;
  lastMinuteChecked = m;

  Serial.print("🕒 ");
  Serial.print(h); Serial.print(":"); Serial.println(m);

  int minutosActual = h * 60 + m;

  for (int i = 0; i < cantidadHorarios; i++) {
    int minutosHorario = horarios[i].hora * 60 + horarios[i].minuto;

    int minutosPre = minutosHorario - 5;
    if (minutosPre < 0) minutosPre += 1440;  // wrap medianoche

    int minutosPost = minutosHorario + 5;
    if (minutosPost >= 1440) minutosPost -= 1440;

    // PRE: 5 minutos antes
    if (minutosActual == minutosPre && !horarios[i].preAvisado) {
      Serial.print("⏰ Aviso PRE para ");
      Serial.print(horarios[i].hora);
      Serial.print(":");
      Serial.println(horarios[i].minuto);

      enviarAvisoHorario(i, "pre");
      horarios[i].preAvisado = true;
    }

    // SERVICIO: minuto exacto
    if (minutosActual == minutosHorario && !horarios[i].ejecutado) {
      servirPorHorario(i);
    }

    // POST: 5 minutos después
    if (minutosActual == minutosPost && !horarios[i].postAvisado) {
      Serial.print("⏰ Aviso POST para ");
      Serial.print(horarios[i].hora);
      Serial.print(":");
      Serial.println(horarios[i].minuto);

      enviarAvisoHorario(i, "post");
      horarios[i].postAvisado = true;
    }
  }

  // Reset diario a medianoche
  if (h == 0 && m == 0) {
    for (int i = 0; i < cantidadHorarios; i++) {
      horarios[i].ejecutado   = false;
      horarios[i].preAvisado  = false;
      horarios[i].postAvisado = false;
    }
    Serial.println("🔁 Reset diario");
  }
}

/*************** SETUP ***************/
void setup() {
  Serial.begin(115200);
  delay(1000);

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);

  myServo.attach(SERVO_PIN);
  myServo.write(10);

  myServo2.attach(SERVO2_PIN);
  myServo2.write(170);  // posición cerrada para el invertido

  Serial.print("Conectando a WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }

  Serial.println("\nWiFi conectado!");
  Serial.println(WiFi.localIP());

  mqttClient.setServer(mqttServer, mqttPort);
  mqttClient.setCallback(mqttCallback);

  timeClient.begin();
  timeClient.update();
  Serial.println("NTP iniciado");

  balanza.begin(HX_DOUT, HX_SCK);
  delay(2000);
  lecturaCero = balanza.read_average(150);
  Serial.print("Cero balanza: ");
  Serial.println(lecturaCero);

  cantidadHorarios = 0;
}

/*************** LOOP ***************/
void loop() {
  if (!mqttClient.connected()) reconnectMQTT();
  mqttClient.loop();

  revisarHorarios();
}