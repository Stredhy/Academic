
#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "Wokwi-GUEST";
const char* password = "";

const char* mqtt_server = "broker.emqx.io";
const int mqtt_port = 1883;

const char* topic = "practica/esp32/sensor";

WiFiClient espClient;
PubSubClient client(espClient);

void conectarWiFi() {
  WiFi.begin(ssid, password, 6);

  Serial.print("Conectando a WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi conectado");
  Serial.println(WiFi.localIP());
}

void conectarMQTT() {
  while (!client.connected()) {
    Serial.print("Conectando a MQTT...");

    String clientId = "ESP32-" + String(random(0xffff), HEX);

    if (client.connect(clientId.c_str())) {
      Serial.println("Conectado");
    } else {
      Serial.print("Error: ");
      Serial.println(client.state());
      delay(2000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  randomSeed(micros());

  conectarWiFi();

  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!client.connected()) {
    conectarMQTT();
  }

  client.loop();

  float temperatura = random(200, 350) / 10.0;
  int led = random(0, 2);

  String mensaje = "{";
  mensaje += "\"temperatura\":";
  mensaje += String(temperatura, 1);
  mensaje += ",\"led\":";
  mensaje += String(led);
  mensaje += "}";

  client.publish(topic, mensaje.c_str());

  Serial.println("Publicado: " + mensaje);

  delay(3000);
}
