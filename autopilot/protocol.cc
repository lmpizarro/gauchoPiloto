const int HARD_BAUD_RATE = 9600;
const int MAX_BYTES  = 4;

class floatToHex
{
    private:
        float minF;
        float maxF;
        uint32_t max_int;
        float p;
        float b;
        uint32_t n_byteI;
	char hexDigits [16] = {'0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'};
    public:
	char hexs[MAX_BYTES * 2 + 1];
        floatToHex (float, float, uint32_t);
        uint32_t floatToInt (float f);
	void printParam ();
        void intToHex (uint32_t);
};

floatToHex::floatToHex (float min_, float max_, uint32_t n_byteI_ ){
    minF = min_;
    maxF = max_;
    n_byteI = n_byteI_;
    uint32_t a = 1; 
    max_int = (a << (n_byteI * 8)) -1;
    p = (float) max_int /(maxF - minF);
    b = - minF * p;

}

uint32_t floatToHex::floatToInt (float f){
  return max(0, min(f*p + b, max_int));
}

void floatToHex::printParam (){
    Serial.println (minF);
    Serial.println (maxF);
    Serial.println (p);
    Serial.println (b);
    Serial.println (max_int);
    Serial.println (n_byteI);
}

//
// Convierte un int a 4 char ascii 0 a F
//
void floatToHex::intToHex (uint32_t temp)
{
    uint32_t i;
    for (i=0; i < n_byteI * 2; i++){
        hexs[n_byteI * 2 - 1 - i] = hexDigits[temp & 0x000F];
        temp = temp >> 4;
    }
    hexs[i] = '\0';

}



floatToHex fToH(1.0, 2.0, 2);
void setup()
{
    // Open serial communications and wait for port to open:
    Serial.begin(HARD_BAUD_RATE);
}

void loop()
{
    delay(1000);
    //fToH.printParam();
    uint32_t intf;
    for (int i = 0; i < 100; i++){
        delay (100);
        intf = fToH.floatToInt(1.0 + i*0.01);
        fToH.intToHex(intf);
	Serial.print(1.0 + i*0.01);
	Serial.print( "   ");
        Serial.println(String(fToH.hexs));

	//Serial.print( "   ");
        //Serial.println(intf);
    }	
}
