/*  ARDUINO SIDE 6-AXIS ROBOTIC ARM WITH SERIALTRANSFER (power_broker)
 *   manages the arduino side of controlling a robotic arm through 
 *   Python, using the library SerialTransfer
 *   
 *   
*/
#include <Servo.h>
#include "SerialTransfer.h"
/*
 * max_servos:    number of joints on the robot
 * servo_pins:    pins connected to signal of each servo, from J0 to J[max_servos]
 * servo_bounds:  the max/min angle position of each servo. 
 *                specific to each robot arm.
 *                [0][servo]: lower limit     [1][servo]: upper limit
*/
const int max_servos = 6; 
const int servo_pins[max_servos] = {7,6,5,3,2,4};//j0(base),j1(arm base),j2,j3,j4,j5
const uint8_t servo_bounds[2][max_servos]={{45  ,97,96 ,180,20 ,180} //lower bound
                                          ,{145 ,0 ,180,0  ,180,0  }};//upper bound
/*
 * curr_pwm:    current position of each servo. starting from J0-J[max_servo]
 *              defined values are the initial position the robot is 
 *              assumed to be in on startup.
 * curr_mapped: current angle translated into 0-100 range. 
 *              used as feedback to Python.
 * targ_mapped: the desired new position the servos are supposed
 *              to move to as a 0-100 value. This is revieced from
 *              Python and to the arduino as input.
 *              value is contrained then mapped to targ_pwm
 * targ_pwm:    desired new position as servo angle. 
 *              used when comparing curr_pwm and targ_pwm
 *              to reach new desired position from current position.
 *              default values same as curr_pwm.
*/
SerialTransfer myTransfer;
Servo servo_array[max_servos];
short curr_pwm[max_servos] = {95,95,96,95,95,95}; //init values;
short curr_mapped[max_servos];
short targ_mapped[max_servos];
short targ_pwm[max_servos] = {95,95,96,95,95,95}; //init values;


void setup() {
  Serial.begin(115200);
  myTransfer.begin(Serial);
  //set up servos
  for(int a = 0; a < max_servos; a++){
    servo_array[a].attach(servo_pins[a]);
  }
}

/*  MAPPING
 *  converting recieved 0-100 position to servo absolute positions
 *  converting processed current servo position to 0-100
*/
void map_targ(){
  for(int a=0;a<max_servos;a++){
    targ_mapped[a] = constrain(targ_mapped[a],0,100);
    targ_pwm[a] = map(targ_mapped[a],0,100,servo_bounds[0][a],servo_bounds[1][a]);
  }//targ mapped -> pwm end
}
void map_curr(){
  for(int a=0;a<max_servos;a++){
    curr_mapped[a] = map(curr_pwm[a],servo_bounds[0][a],servo_bounds[1][a],0,100);
  }//current pwm -> mapped end
}
///////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////

/*  SERVO COMMANDER
 *   sends new commands to servos
 *   increments the steps of current angle until it reaches target
 *   MUST be run repetitively, no sleep allowed
 *   MUST be run after mapping target func (map_targ())
*/
void servo_comm(){
  //loop through all servos
  for(int servo_num = 0; servo_num < max_servos; servo_num++){
    //compare and increment up or down respectively
    if(curr_pwm[servo_num] < targ_pwm[servo_num]){
      curr_pwm[servo_num]++;
    }else if(curr_pwm[servo_num] > targ_pwm[servo_num]){
      curr_pwm[servo_num]--;
    }
    //curr_pwm[servo_num] = constrain(curr_pwm[servo_num],servo_bounds[0][servo_num],servo_bounds[1][servo_num]);
  //send the command
    servo_array[servo_num].write(curr_pwm[servo_num]);
  }
  map_curr();//update current values
}
///////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////

/*  RESPONSE
 *   responds to the serial port
 *   returns the current servo positions
 *   can send 0-100 values or servo angle by changing curr_mapped
 *   to curr_mapped (for 0-100) or curr_pwm (servo angle)
*/
void serial_respond(bool respond){
  if(respond){
    for(int servo_num=0;servo_num<max_servos;servo_num++){
      myTransfer.packet.txBuff[servo_num] = curr_mapped[servo_num];
    }
    myTransfer.sendData(max_servos);
  }
}
///////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////

/*  MAIN LOOP
 *   if data rcv
 *      copy target pos over locally
 *   update servos
*/
void loop() {
  bool ser_respond = false;
  if(myTransfer.available())
  {
    for(int a=0;a<max_servos;a++){
      targ_mapped[a] = myTransfer.packet.rxBuff[a];
    }
    map_targ();
    ser_respond = true;
  }

  servo_comm();
  serial_respond(ser_respond);
  //error |= update_Servo(error);
  //error |= error_check(error);

  delay(30); //give time for servos to move
}
///////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////

/*  ERROR CHECKER
 *   checks for errors that occured
 *   
*/
uint8_t error_check(uint8_t error){
  if(error){
    if((error & 1)==1)    {Serial.println("");}
    if((error & 2)==2)    {Serial.println("");}
    if((error & 4)==4)    {Serial.println("");}
    if((error & 8)==8)    {Serial.println("");}
    if((error & 16)==16)  {Serial.println("");}
    if((error & 32)==32)  {Serial.println("");}
    if((error & 64)==64)  {Serial.println("");}
    if((error & 128)==128){Serial.println("");}
  } else {
    Serial.println("no error");
  }
  //reset error
  return 0;
}
