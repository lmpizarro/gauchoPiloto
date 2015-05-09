#ifndef PID_H_
#define PID_H_

class PID
{
    private:
        float k_p;
	float k_d;
	float k_i;
	float input;
	float output;
	float sum_i;
	float input_0;

    public:
        PID(float, float, float);
	void update(float);
	void reset_I();
};



#endif /*PID_H_*/
