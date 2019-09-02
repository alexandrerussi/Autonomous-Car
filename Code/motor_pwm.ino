//Carrega a biblioteca do sensor ultrassonico
#include <Ultrasonic.h>
 
//Define os pinos para o trigger e echo
#define pino_trigger 4
#define pino_echo 5
 
//Inicializa o sensor nos pinos definidos acima
Ultrasonic ultrasonic(pino_trigger, pino_echo);

//Definicoes pinos Arduino ligados a entrada da Ponte H
int IN1 = 6;
int IN2 = 9;
int IN3 = 10;
int IN4 = 11;
int incomingByte = 0;


void setup()
{
  //Define os pinos como saida
 pinMode(IN1, OUTPUT);
 pinMode(IN2, OUTPUT);
 pinMode(IN3, OUTPUT);
 pinMode(IN4, OUTPUT);
 Serial.begin(9600);
}

void liga_motorA_horario(){
   //Gira o Motor A no sentido horario
   digitalWrite(IN1, HIGH);
   digitalWrite(IN2, LOW);
   delay(2000);
   //Para o motor A
   digitalWrite(IN1, HIGH);
   digitalWrite(IN2, HIGH);
   delay(500);
}

void liga_motorA_antihorario(){
    //Gira o Motor A no sentido anti-horario
   digitalWrite(IN1, LOW);
   digitalWrite(IN2, HIGH);
   delay(2000);
   //Para o motor A
   digitalWrite(IN1, HIGH);
   digitalWrite(IN2, HIGH);
   delay(500);
}

void liga_motorB_horario(){
   //Gira o Motor B no sentido horario
   analogWrite(IN3, 0);     
   analogWrite(IN4, 108);
   delay(2000);
   analogWrite(IN3, 0);     
   analogWrite(IN4, 0);
}

void liga_motorB_antihorario(){
   //Gira o Motor B no sentido anti-horario
   analogWrite(IN3, 108);
   analogWrite(IN4, 0);
   delay(2000);
   analogWrite(IN3, 0);     
   analogWrite(IN4, 0);
}

void loop()
{
  float cmMsec, inMsec;
  long microsec = ultrasonic.timing();
  cmMsec = ultrasonic.convert(microsec, Ultrasonic::CM);
  inMsec = ultrasonic.convert(microsec, Ultrasonic::IN);
  //Exibe informacoes no serial monitor
  Serial.print("Distancia em cm: ");
  Serial.print(cmMsec);
  Serial.print(" - Distancia em polegadas: ");
  Serial.println(inMsec);

  if(cmMsec > 10){
    analogWrite(IN3, 0);     
    analogWrite(IN4, 90);
  }else{
    analogWrite(IN3, 0);     
    analogWrite(IN4, 0);
  }
  
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read() - 48;

    // say what you got:
    //Serial.print("I received: ");
    int val = Serial.parseInt(); //read int or parseFloat for ..float...

    Serial.println(val);
    if(incomingByte == 1){
      liga_motorB_antihorario();
    }else{
      if(incomingByte == 2){
        Serial.println("AGORA VAI");
        liga_motorB_horario();
      }else{
        if(incomingByte == 3){
          liga_motorA_horario();    
          Serial.println("AGORA VAI");  
        }else{
          if(incomingByte == 4){
            liga_motorA_antihorario(); 
            Serial.println("AGORA VAI");
          }else{
            Serial.println("NAO RECEBI NADA"); 
          }
        }
      } 
    }
    delay(2000);
  }else{    
    Serial.println("NAO RECEBI NADA");
  }
}
