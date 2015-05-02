#ifndef ahrs_h
#define ahrs_h

#define PI  3.141592654

class AHRS
{

	public:
	  AHRS ();
          void MadgwickQuaternionUpdate(float ax, float ay, float az, float gx, float gy, float gz, float mx, float my, float mz);
          void MahonyQuaternionUpdate(float ax, float ay, float az, float gx, float gy, float gz, float mx, float my, float mz);
	private:
          // gyroscope measurement error in rads/s (shown as 3 deg/s)
	  const float  GyroMeasError =PI * (40.0f / 180.0f);
	  const float beta   = sqrt(3.0f / 4.0f) * GyroMeasError;   // compute beta
	  float  ax, ay, az;
	  float  gx, gy, gz;
	  float  mx, my, mz;
          // these are the free parameters in the Mahony filter and fusion scheme, Kp for proportional feedback, Ki for integral
	  float Ki, Kp;

          float eInt[3] = {0.0f, 0.0f, 0.0f};       // vector to hold integral error for Mahony method
          float q[4] = {1.0f, 0.0f, 0.0f, 0.0f};    // vector to hold quaternion

          float deltat = 0.0f;        // integration interval for both filter schemes

};

#endif
