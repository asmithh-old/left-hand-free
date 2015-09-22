int light = 0;
int flex1 = 0;
int flex2 = 0;
int flex3 = 0;
int flex4 = 0;
int flex5 = 0;
int tilt = 0;
int tap = 0;
boolean calib = false;

void setup() {
  pinMode(A0,INPUT);
  pinMode(A1,INPUT);
  pinMode(A2,INPUT);  
  pinMode(A3,INPUT);
  pinMode(A4,INPUT);
  pinMode(A5,INPUT);
  pinMode(3,INPUT);
  pinMode(4,INPUT);
  Serial.begin(9600);
}

void loop() {
  
  for(int x = 0;x<1000;x++){
    light = analogRead(0);
    flex1 = analogRead(1);
    flex2 = analogRead(2);
    flex3 = analogRead(3);
    flex4 = analogRead(4);
    flex5 = analogRead(5);
    tilt = digitalRead(3);
    tap = digitalRead(4);
    int sensors[] = {light, flex1, flex2, flex3, flex4, flex5, tilt, tap};
    Serial.print('[');
    Serial.print(sensors[0]);
    for(int count = 1; count <8; count++){
      Serial.print(',');
      Serial.print(sensors[count]);
    }
    Serial.print(']');
    Serial.print('\n');
    delay(5);
  }

Serial.println("'calibration done'");
  calib = true;

  while(calib == true){
    light = analogRead(0);
    flex1 = analogRead(1);
    flex2 = analogRead(2);
    flex3 = analogRead(3);
    flex4 = analogRead(4);
    flex5 = analogRead(5);
    tilt = digitalRead(3);
    tap = digitalRead(4);
    int sensors[] = {light, flex1, flex2, flex3, flex4, flex5, tilt, tap};
   Serial.print('[');
    Serial.print(sensors[0]);
    for(int count = 1; count <8; count++){
      Serial.print(',');
      Serial.print(sensors[count]);
    }
    Serial.print(']');
    Serial.print('\n');
    delay(200);
  }
  // put your main code here, to run repeatedly:
}
