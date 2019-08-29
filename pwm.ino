/*
Controle de velocidade de motor DC com PWM
Autores: Pedro Bertoleti e FilipeFlop
*/
 
#define PINO_PWM                      9    //pino do Arduino que terá a ligação para o driver de motor (ponte H) L298N)
#define TEMPO_NA_MESMA_VELOCIDADE     300  //tempo (ms) em que o motor ficara na mesma velocidade 
  
void setup()
{ 
    //configura como saída pino terá a ligação para o driver de motor (ponte H) L298N)
    pinMode(PINO_PWM, OUTPUT);
}
  
void loop()
{   
    int valor_pwm = 0;   //variavel que armazena o valor do PWM (0..255 -> 0%..100% da rotação do motor) 
 
    //Aumento de velocidade (0%..100%)
    //for (valor_pwm = 0; valor_pwm < 256; valor_pwm++)
    //{
        analogWrite(9, 0);
        analogWrite(6, 108);
        //delay(TEMPO_NA_MESMA_VELOCIDADE);
        delay(5000);
    //}
 
    //Diminuição de velocidade (100%..0%)
    //for (valor_pwm = 255; valor_pwm >= 0; valor_pwm--)
    //{
        analogWrite(9, 108);
        analogWrite(6, 0);
        delay(5000);
        //delay(TEMPO_NA_MESMA_VELOCIDADE);
    //}
}
