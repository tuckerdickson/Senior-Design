/* 
 *  A digital frequency selective filter
 *  A. Kruger, 2019
 *  revised R. Mudumbai, 2020
 */
 
// The following defines are used for setting and clearing register bits on the Arduino processor. Low-level stuff: leave alone.
#ifndef cbi
#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))
#endif

#ifndef sbi
#define sbi(sfr, bit) (_SFR_BYTE(sfr) |= _BV(bit))
#endif

int analogPin = XXX;                                      // Specify analog input pin. Make sure to keep between 0 and 5V.
int LED = XXX;                                            // Specify output analog pin with indicator LED 

// a and b are the numerator and denominator coeffs of a digital frequency-selective filter designed for a sample rate XXX
int n = 3;                                                // number of past input and output samples to buffer; change this to match order of your filter
float a[] = {  1.00e+000, -1.3272e+000, 876.80e-003};	    // array size <= n; make it n and pad with zeros as needed
float b[] = {937.50e-003, -1.3272e+000, 937.50e-003};	    // array size <= n as above
    
float x[3],y[3],yn;                                       // Space to hold previous samples and outputs; n'th order filter will require up to n samples buffered

void setup() {
   int i;

   sbi(ADCSRA,ADPS2);     // Next three lines make the ADC run faster
   cbi(ADCSRA,ADPS1);
   cbi(ADCSRA,ADPS0);

   pinMode(LED,OUTPUT);   // Makes the LED pin an output

   for (i=0; i<n; i++)
      x[i] = y[i] = 0;
      
   yn = 0;
}

void loop() {
   unsigned long t1;
   int i,count,val;
   int k=0;

   count = 0;

   while (1) {
      t1 = micros();
      
      // Calculate the next value of the difference equation.
      for(i=1; i<n; i++){             // Shift samples
         x[i] = x[i-1];                                            
         y[i] = y[i-1];
      }

      val = analogRead(analogPin);  // New input
      x[0] = val*(5.0/1023.0)-2.5;  // Scale to match ADC resolution and range

      yn = 0;
      
      for(i=0;i<n;i++)             // Incorporate inputs (x[n])
         yn = yn + b[i]* x[i];  

      for(i=1;i<n;i++)             // Incorporate previous outputs (y[n])
         yn = yn - a[i]* y[i];          

       y[0] = yn;                  // New output


      /*
       * The variable yn is the output of the filter at this time step.
       * Now we can use it for its intended purpose:
       *     - Apply theshold
       *     - Apply hysteresis
       *     - What to do when the beam is interrupted, turn on a buzzer, send SMS alert.
       *     - etc.
       *     
       * Absolute value of the filter output. XXX do something with yn
       * float s = abs(2*yn);
       * 
       * The filter was designed for a XXX Hz sampling rate. This corresponds
       * to a sample every XXX us. The code above must execute in less time
       * (if it doesn't, it is not possible to do this filtering on this processor).
       * Below we tread some water until it is time to process the next sample
       */

      while((micros()-t1) < XXX)
        ;  
   }
}
