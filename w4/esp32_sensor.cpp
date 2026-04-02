#include <Arduino.h>
#include <DHTesp.h>
#include <LiquidCrystal_I2C.h>

#define DHT_PIN 13
#define PIR_PIN 15
#define LED_PIN 2

DHTesp dht;
LiquidCrystal_I2C lcd(0x27, 16, 2); 

unsigned long lastReadTime = 0;
const unsigned long readInterval = 2000; 

void setup() {
  Serial.begin(115200);
  pinMode(PIR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  
  dht.setup(DHT_PIN, DHTesp::DHT22);
  lcd.init();
  lcd.backlight();

  lcd.setCursor(0, 0);
  lcd.print("ESP32 DHT22 PIR");
  lcd.setCursor(0, 1);
  lcd.print("Khoi dong...");
  delay(2000);
  lcd.clear();

  Serial.println("ESP32 READY");
}

void loop() {
  unsigned long currentTime = millis();

  // Đọc dữ liệu DHT22 mỗi 2 giây 
  if (currentTime - lastReadTime >= readInterval) {
    lastReadTime = currentTime;

    TempAndHumidity data = dht.getTempAndHumidity();
    if (isnan(data.temperature) || isnan(data.humidity)) {
      Serial.println("Loi doc DHT22!");
      return;
    }

    // Hiển thị lên LCD
    lcd.setCursor(0, 0);
    lcd.print("Nhiet:");
    lcd.print(data.temperature, 1);
    lcd.print("C   ");

    lcd.setCursor(0, 1);
    lcd.print("Do am:");
    lcd.print(data.humidity, 1);
    lcd.print("%   ");

    // Gửi log qua Serial
    Serial.printf("[LOG] Nhiet do: %.1f*C | Do am: %.1f%%\n", data.temperature, data.humidity);
  }

  //  Kiểm tra PIR 
  int pirState = digitalRead(PIR_PIN);
  if (pirState == HIGH) {
    digitalWrite(LED_PIN, HIGH);
    Serial.println("[PIR] Phat hien chuyen dong! LED ON");
  } else {
    digitalWrite(LED_PIN, LOW);
    Serial.println("[PIR] Khong co chuyen dong. LED OFF");
  }

  delay(200); // Giảm tốc độ log Serial, tránh tràn
}
