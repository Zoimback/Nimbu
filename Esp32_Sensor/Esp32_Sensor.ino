#include <OneWire.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h> // Agrega la librería ArduinoJson

// Pin de datos del sensor
#define PIN_DAT 15

// Objeto de la clase OneWire
OneWire oneWire(PIN_DAT);
char ssid[] = "Livebox6-78BF";    // your SSID
char pass[] = "UPQ3b9ckshRG"; 
String serverName = "http://192.168.1.20:5000/insert";

WiFiClient client;

void setup() {
  Serial.begin(9600);
  
  // Begin WiFi section
  WiFi.begin(ssid, pass);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  
  Serial.println("Connected to network");
  
  IPAddress ip = WiFi.localIP();
  Serial.print("My IP address is: ");
  Serial.println(ip);
  Serial.println("Connecting...");
}

void loop() {
  // Variables para almacenar los datos leídos del sensor
  byte direccion[8];
  byte tipo;
  byte datos[12];
  float temperatura;

  // Busca el sensor y obtiene su dirección
  if (!oneWire.search(direccion)) {
    // Si no se encuentra el sensor, se reinicia la búsqueda
    oneWire.reset_search();
    return;
  }
  
  // Inicia la conversión de temperatura
  oneWire.reset();
  oneWire.select(direccion);
  oneWire.write(0x44);

  // Espera a que termine la conversión de temperatura
  delay(750);

  // Lee los datos de temperatura del sensor
  oneWire.reset();
  oneWire.select(direccion);
  oneWire.write(0xBE);
  for (byte i = 0; i < 9; i++) {
    datos[i] = oneWire.read();
  }

  // Calcula la temperatura a partir de los datos leídos
  temperatura = ((datos[1] << 8) | datos[0]) * 0.0625;

  // Imprime la temperatura en la consola
  Serial.print("Temperatura: ");
  Serial.print(temperatura);
  Serial.println(" °C");

  // Crea el objeto HTTPClient
  HTTPClient http;

  // Crea un objeto JSON
StaticJsonDocument<200> jsonDoc;
jsonDoc["temp"] = temperatura;
jsonDoc["esp"] = "test sensor-1";

// Serializa el JSON en un buffer
String jsonString;
serializeJson(jsonDoc, jsonString);

// Realiza la solicitud POST al servidor con los datos del JSON
http.begin(serverName.c_str());
http.addHeader("Content-Type", "application/json"); // Establece el encabezado de contenido como JSON
int httpResponseCode = http.POST(jsonString);

  if (httpResponseCode > 0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    String response = http.getString();
    Serial.println(response);
  } else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }

  // Libera los recursos
  http.end();
  
  // Espera 1 segundo antes de volver a leer la temperatura
  delay(150000);
}
