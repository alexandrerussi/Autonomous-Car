//Definicoes pinos Arduino ligados a entrada da Ponte H
int IN1 = 4;
int IN2 = 5;
int IN3 = 6;
int IN4 = 7;
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
 //Gira o Motor A no sentido horario
   digitalWrite(IN1, HIGH);
   digitalWrite(IN2, LOW);
   delay(2000);
   //Para o motor A
   digitalWrite(IN1, HIGH);
   digitalWrite(IN2, HIGH);
   delay(500);
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
   digitalWrite(IN3, HIGH);
   digitalWrite(IN4, LOW);
   delay(2000);
   //Para o motor B
   digitalWrite(IN3, HIGH);
   digitalWrite(IN4, HIGH);
   delay(500);
}

void liga_motorB_antihorario(){
    //Gira o Motor B no sentido anti-horario
   digitalWrite(IN3, LOW);
   digitalWrite(IN4, HIGH);
   delay(2000);
   //Para o motor B
   digitalWrite(IN3, HIGH);
   digitalWrite(IN4, HIGH);
   delay(500);
}

void loop()
{
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
        }else{
          if(incomingByte == 4){
            liga_motorA_antihorario(); 
          }else{
            Serial.println("NAO RECEBI NADA"); 
          }
        }
      } 
    }
    delay(2000);
  }
}
