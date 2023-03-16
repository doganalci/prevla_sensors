


#include "ros/ros.h"
#include "visualization_msgs/Marker.h"
#include "visualization_msgs/MarkerArray.h"

#include "leap_motion/Human.h"
#include "leap_motion/Hand.h"
#include "leap_motion/Finger.h"
#include "leap_motion/Bone.h"

#include "Leap.h"
#include <iostream>

//////////////////////// radar lib //////////////////
using std::ifstream;
using std::ofstream;

#include <typeinfo>

#include <string>
#include <cstdlib> // for exit function
#include <stdio.h>
#include <chrono>
#include <stdlib.h>
#include<iostream>
////////////////doga
////bag
#include <std_msgs/Int32.h>
#include <rosbag/bag.h>
#include <std_msgs/String.h>
#include "rosbag/bag.h"
////bag

int HND, FNGR, plmind=0,pntind=0,pntind2=0;
float palmx,palmy,palmz;
double palmstamp;
//////////  rowları say //////////////


//////////  rowları say //////////////

#define PCL_NO_PRECOMPILE
void filePutContents(const std::string& name, const std::string& content, bool append = false) {
    std::ofstream outfile;
    if (append)
        outfile.open(name, std::ios_base::app);
    else
        outfile.open(name);
    outfile << content;
}

//////////////////////// radar lib //////////////////


///////////// RADARDAN GELEN OPARAMETRELER //////////////////
/////////////////////////kullanıcı giriş parametreleri
char kimlik[250]="doga";    // kullanıcı adı buraya girilecek
int scale_factor=60; // basılacak ve kaydedilecek resim küçütme oranı
int terminal =1 ;// terminale basılsın mı 1 evet 0 hayır?
int koor_yaz =1 ;// koordinatlar terminale yazılsın mı?
int cam_prt=1;
int image_operation=1;
///////////////////////////////
int hand_no,radar_no;
FILE* fradar;FILE* fimage;FILE* fdeney;

int bbb,bb,cnf=1 ,ffdd=0,t=0,son_radar=0, son_image=0,son_deney=0,il,sy=0;
char bas[250]="",buffer [250], buffer2 [250],buffer_cfg [1000];
std::ofstream outdata,cvsdata; // outdata is like cin
std::ifstream ifs;
double fractional_seconds_since_epoch;
double fractional_seconds_since_epoch2;
///////////// RADARDAN GELEN OPARAMETRELER //////////////////


int ip=0;
static ros::Publisher* marker_pub;
const std::string fingerNames[] = {"Thumb", "Index", "Middle", "Ring", "Pinky"};

/*!
 * \brief Adds circles at the intersection of bones
 * 
 * Takes a pointer to human.msg, and a start of a bone. Using that information creates a
 * sphere visualization marker that will later be appended to a marker array.
 * 
 * \param human     Pointer to the received Human.msg
 * \param hand_ns   Used to create a unique namespace
 * \param finger_ns Used to create a unique namespace
 * \param location  Tip position of a bone object 
 */
visualization_msgs::Marker createJointMarker(const leap_motion::Human::ConstPtr& human, 
    std::string hand_ns, std::string finger_ns, unsigned int id, geometry_msgs::Pose location ){

    visualization_msgs::Marker joint_marker;

    joint_marker.header.frame_id = human->header.frame_id;
    joint_marker.header.stamp = human->header.stamp;
    joint_marker.ns = hand_ns+"_"+finger_ns;
    joint_marker.id = id;
    joint_marker.type =  visualization_msgs::Marker::SPHERE;
    joint_marker.action = visualization_msgs::Marker::ADD;

    // Location data in meters from origin
    joint_marker.pose.position.x = location.position.x;
    joint_marker.pose.position.y = location.position.y; 
    joint_marker.pose.position.z = location.position.z;

    joint_marker.scale.x = 0.015;
    joint_marker.scale.y = 0.015;
    joint_marker.scale.z = 0.015;
    
    joint_marker.color.r = 1.0f;
    joint_marker.color.g = 0.0f;
    joint_marker.color.b = 0.0f;
    joint_marker.color.a = 1.0f;
    joint_marker.lifetime = ros::Duration(0.1);



if (true){

 std::cout <<  "joint_marker.ns----------> "<<  joint_marker.ns << "\n";
 std::cout <<  "joint_marker.type--------> "<<  joint_marker.type << "\n";
 std::cout <<  "joint_marker.id----------> "<<  joint_marker.id << "\n";
 std::cout <<  "joint_marker.action------> "<<  joint_marker.action << "\n";
 std::cout <<  "hands_ns-----------------> "<<  hand_ns << "\n";
 std::cout <<  "finger_ns----------------> "<<  finger_ns << "\n";
 std::cout <<  "human--------------------> "<<  human << "\n"<<std::endl;
 std::cout <<  "location.x---------------> "<<  location.position.x<< "\n";
 std::cout <<  "location.y---------------> "<<  location.position.y<< "\n";
 std::cout <<  "location.z---------------> "<<  location.position.z<< "\n"<<std::endl;
 std::cout <<  "orientation.x------------> "<<  location.orientation.x<< "\n";
 std::cout <<  "orientation.y------------> "<<  location.orientation.y<< "\n";
 std::cout <<  "orientation.z------------> "<<  location.orientation.z<< "\n";
 std::cout <<  "orientation.w------------> "<<  location.orientation.w<< "\n"<<std::endl;
 std::cout <<  "palx---------------------> "<<  palmstamp<<std::endl;
 std::cout <<  "palx---------------------> "<<  palmx<<std::endl;
 std::cout <<  "paly---------------------> "<<  palmy<<std::endl;
 std::cout <<  "palz---------------------> "<<  palmz<<std::endl<<std::endl;



  
}
//char jm_ns[20 + sizeof(char)];std::sprintf(jm_ns, "%s", joint_marker.ns);


//printf("joint_marker.ns-- %s\n" ,joint_marker.ns);
//std::cout<<"joint_marker.ns--"<<joint_marker.ns<<"\n";

//std::string jm_ns = std::format(joint_marker.ns);

  if (hand_ns=="Right")HND=0;
    else HND=1;
    

for (int yy=0;yy<5;yy++){
ffdd+=1;

if(fingerNames[yy]==finger_ns) {FNGR=yy;break;}
  
    
}

std::cout<<"HND  "<<HND<<"\n";
std::cout<<"FNG  "<<FNGR<<"\n";

std::ostringstream ss;
ss << joint_marker.ns;
std::string jm_ns = ss.str();


std::cout<<"jm_ns--"<<jm_ns<<"\n";

//std::cout << typeid(jm_ns).name() << std::endl;

//cvsdata.open("/home/doga18/Desktop/prevla_leap_doga/catkin_ws/log/radar_data_doga.csv",std::ios_base::app); // opens the file
// Usage example: filePutContents("./yourfile.txt", "content", true);
            fractional_seconds_since_epoch=std::chrono::duration_cast<std::chrono::duration<double>>(        std::chrono::system_clock::now().time_since_epoch()).count();

bbb=sprintf (buffer,"%f,%f,%d,%d,%d,%d,%d,%d,%d,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n",palmstamp,fractional_seconds_since_epoch,plmind,pntind,pntind2,HND,FNGR,joint_marker.id,joint_marker.type,location.position.x,location.position.y,location.position.z,location.orientation.x,location.position.x,location.orientation.z,location.orientation.w,palmx,palmy,palmx);
//bbb=sprintf (buffer,"%f,%f,%f,%f,%f,%f,%f,\n",location.position.x,location.position.y,location.position.z,location.orientation.x,location.position.x,location.orientation.z,location.orientation.w);
//std::cout<<"bbb------------------------------> "<<bbb<<std::endl;
//std::cout<< "BUFFER  ::"<<buffer<<std::endl;
//outdata<<buffer;
//cvsdata<<buffer;
filePutContents("/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/log/radar_data_doga.csv",buffer,true);
pntind++;
if (pntind%23==0) {pntind2++;}

int bag=0;



if (1==1){  // 5-9 ARASI    
printf("[DOGA_INFO]     basla\n");
printf("[DOGA_INFO]     ip                            --> %d\n",    ip++);
printf("[DOGA_INFO]     joint_marker.lifetime         --> %d\n",    joint_marker.lifetime);
printf("[DOGA_INFO]     joint_marker.header.stamp     --> %d\n",    joint_marker.header.stamp);
printf("[DOGA_INFO]     joint_marker.pose             --> %s\n\n",    joint_marker.pose);
if (1==0){
//printf("[DOGA_INFO]     joint_marker.action           --> %d\n",     joint_marker.action);
//printf("[DOGA_INFO]     joint_marker.typ              --> %f\n",   joint_marker.type);
//printf("[DOGA_INFO]     joint_marker.id               --> %d\n",    joint_marker.id);
//printf("[DOGA_INFO]     hand_ns                       --> %s\n",   hand_ns);
//printf("[DOGA_INFO]     finger_ns                     --> %s\n",   finger_ns);
//printf("[DOGA_INFO]     joint_marker.ns               --> %s\n",   joint_marker.ns);
//printf("[DOGA_INFO]     joint_marker.header.frame_id  --> %d\n",    joint_marker.header.frame_id);



for (int yy=0;yy<1;yy++){
printf("[DOGA_INFO]     joint_marker.pose.position.x  --> %f\n",    joint_marker.pose.position.x);
printf("[DOGA_INFO]     joint_marker.pose.position.y  --> %f\n",    joint_marker.pose.position.y);
printf("[DOGA_INFO]     joint_marker.pose.position.z  --> %f\n",    joint_marker.pose.position.z);
printf("[DOGA_INFO]     bitir\n");
}
printf("\njoint_marker -> %d\n",joint_marker);
}
}
    return joint_marker;
}

/*!
 * \brief Adds lines between the tips of the bones.
 * 
 * Takes a pointer to human.msg, and a bone.msg. Using that information
 * adds lines between the tips of the bones.
 * 
 * \param human         Pointer to the received Human.msg
 * \param hand_ns       Used to create a unique namespace
 * \param finger_ns     Used to create a unique namespace
 * \param current_bone  The bone that will be represented as a line.
 */
visualization_msgs::Marker createFingerLines(const leap_motion::Human::ConstPtr &human, 
    std::string hand_ns, std::string finger_ns, unsigned int id, leap_motion::Bone current_bone){
    
    visualization_msgs::Marker line_list;
    line_list.header.frame_id = human -> header.frame_id;
    line_list.header.stamp = human -> header.stamp;
    line_list.ns = hand_ns + "_" + finger_ns;
    line_list.type = visualization_msgs::Marker::LINE_LIST;
    line_list.action = visualization_msgs::Marker::ADD;
    line_list.id = id;

    line_list.scale.x = 0.0075;

    // Line list is white
    line_list.color.r = 1.0f;
    line_list.color.g = 1.0f;
    line_list.color.b = 1.0f;
    line_list.color.a = 1.0f;
    line_list.lifetime = ros::Duration(0.1);

    geometry_msgs::Point p;
    p.x = current_bone.bone_start.position.x;
    p.y = current_bone.bone_start.position.y;
    p.z = current_bone.bone_start.position.z;
    line_list.points.push_back(p);

    p.x = current_bone.bone_end.position.x;
    p.y = current_bone.bone_end.position.y;
    p.z = current_bone.bone_end.position.z;
    line_list.points.push_back(p);

    return line_list;
}

/*!
 * \brief Creates a representation of palm
 * 
 * Takes a pointer to human.msg, and a hand.msg. Using that information
 * adds draw lines between fingers to create a palm.
 * 
 * \param human         Pointer to the received Human.msg
 * \param hand_ns       Used to create a unique namespace
 * \param finger_ns     Used to create a unique namespace
 * \param current_hand  The hand from which the palm will be created
 */
visualization_msgs::Marker createHandOutline(const leap_motion::Human::ConstPtr &human, 
    std::string hand_ns, unsigned int id, leap_motion::Hand current_hand){

    visualization_msgs::Marker line_list;
    line_list.header.frame_id = human -> header.frame_id;
    line_list.header.stamp = human -> header.stamp;
    line_list.ns = hand_ns;
    line_list.id = id;
    
    line_list.type = visualization_msgs::Marker::LINE_LIST;
    line_list.action = visualization_msgs::Marker::ADD;

    line_list.scale.x = 0.0075;

    // Line list is white
    line_list.color.r = 1.0f;
    line_list.color.g = 1.0f;
    line_list.color.b = 1.0f;
    line_list.color.a = 1.0f;
    line_list.lifetime = ros::Duration(0.1);

    for(unsigned int j = 0; j < current_hand.finger_list.size(); j++){
        
        geometry_msgs::Point p;

        leap_motion::Finger finger = current_hand.finger_list[j];
        leap_motion::Bone bone = finger.bone_list[0];

        // Connects thumb start and index finger
        if(finger.type == Leap::Finger::Type::TYPE_THUMB)
        {
            p.x = bone.bone_start.position.x;
            p.y = bone.bone_start.position.y;
            p.z = bone.bone_start.position.z;
            line_list.points.push_back(p);

            // Assumption that the hand has all 5 fingers and 
            // that the fingers are given in order from thumb[idx 0] to pinky[idx 4].
            finger = current_hand.finger_list[1];
            bone = finger.bone_list[1];
            p.x = bone.bone_start.position.x;
            p.y = bone.bone_start.position.y;
            p.z = bone.bone_start.position.z;
            line_list.points.push_back(p);
        }
        // Connect wrist and pinky
        else if(finger.type == Leap::Finger::Type::TYPE_PINKY)
        {
            p.x = bone.bone_start.position.x;
            p.y = bone.bone_start.position.y;
            p.z = bone.bone_start.position.z;
            line_list.points.push_back(p);

            p.x = bone.bone_end.position.x;
            p.y = bone.bone_end.position.y;
            p.z = bone.bone_end.position.z;
            line_list.points.push_back(p);

            // Creates the line from index to pinky at the wrist
            p.x = bone.bone_start.position.x;
            p.y = bone.bone_start.position.y;
            p.z = bone.bone_start.position.z;
            line_list.points.push_back(p);

            finger = current_hand.finger_list[0];
            bone = finger.bone_list[0];

            p.x = bone.bone_start.position.x;
            p.y = bone.bone_start.position.y;
            p.z = bone.bone_start.position.z;
            line_list.points.push_back(p);
        }
        else
        {   
            // Connects current finger and the follwing finger at the start of proximal bone (id 1)
            leap_motion::Bone bone = finger.bone_list[1];
            p.x = bone.bone_start.position.x;
            p.y = bone.bone_start.position.y;
            p.z = bone.bone_start.position.z;
            line_list.points.push_back(p);

            leap_motion::Finger temp_finger = current_hand.finger_list[j+1];
            bone = temp_finger.bone_list[1];
            p.x = bone.bone_start.position.x;
            p.y = bone.bone_start.position.y;
            p.z = bone.bone_start.position.z;
            line_list.points.push_back(p);

        }
    }
    geometry_msgs::Point p;
    p.x = current_hand.arm.elbow.position.x;
    p.y = current_hand.arm.elbow.position.y;
    p.z = current_hand.arm.elbow.position.z;
    line_list.points.push_back(p);
    p.x = current_hand.arm.wrist.position.x;
    p.y = current_hand.arm.wrist.position.y;
    p.z = current_hand.arm.wrist.position.z;
    line_list.points.push_back(p);


    return line_list;
}

/*!
 * \brief Represents the midpoint of the palm
 * 
 * Takes a pointer to human.msg, and pose the the centre point of the palm. 
 * Using that information creates a sphere at that location.
 * 
 * \param human         Pointer to a received Human.msg
 * \param hand_ns       Used to create a unique namespace
 * \param id            A unique id to the created marker
 * \param centre_point  The palm centre of a hand
 */
visualization_msgs::Marker createPalmPosition(const leap_motion::Human::ConstPtr &human, 
    std::string hand_ns, unsigned int id, geometry_msgs::Point centre_point){
    
    visualization_msgs::Marker palm_centre;
    palm_centre.header.frame_id = human -> header.frame_id;
    palm_centre.header.stamp = human -> header.stamp;

    palm_centre.ns = hand_ns;
    palm_centre.id = id;
    palm_centre.type = visualization_msgs::Marker::SPHERE;
    palm_centre.action = visualization_msgs::Marker::ADD;

    // Location data in meters from origin
    palm_centre.pose.position.x = centre_point.x;
    palm_centre.pose.position.y = centre_point.y; 
    palm_centre.pose.position.z = centre_point.z;

    palmx=palm_centre.pose.position.x;
    palmy=palm_centre.pose.position.y;
    palmz=palm_centre.pose.position.z;
    palmstamp=std::chrono::duration_cast<std::chrono::duration<double>>(        std::chrono::system_clock::now().time_since_epoch()).count();



    palm_centre.scale.x = 0.025;
    palm_centre.scale.y = 0.025;
    palm_centre.scale.z = 0.025;

 
   
    palm_centre.color.r = 0.0f;
    palm_centre.color.g = 0.0f;
    palm_centre.color.b = 1.0f;
    palm_centre.color.a = 1.0f;
    palm_centre.lifetime = ros::Duration(0.1);

    printf("[DOGA_INFO]     palem_centre.x         --> \n");
    printf("[DOGA_INFO]     palm_centre.pose.position.x         --> %f\n",    palm_centre.pose.position.x);
    printf("[DOGA_INFO]     palm_centre.pose.position.y         --> %f\n",    palm_centre.pose.position.y);
    printf("[DOGA_INFO]     palm_centre.pose.position.z         --> %f\n",    palm_centre.pose.position.z);
    printf("[DOGA_INFO]     palm_centre.header.stamp            --> %f\n",    palm_centre.header.stamp);
    printf("[DOGA_INFO]     palm_centre.header.frame_id         --> %f\n",    palm_centre.header.frame_id );
fractional_seconds_since_epoch2=std::chrono::duration_cast<std::chrono::duration<double>>(        std::chrono::system_clock::now().time_since_epoch()).count();

bbb=sprintf (buffer2,"%f,%d,%f,%f,%f\n", fractional_seconds_since_epoch2,plmind,palm_centre.pose.position.x,palm_centre.pose.position.y,palm_centre.pose.position.z);
plmind++;
//bbb=sprintf (buffer,"%f,%f,%f,%f,%f,%f,%f,\n",location.position.x,location.position.y,location.position.z,location.orientation.x,location.position.x,location.orientation.z,location.orientation.w);
//std::cout<<"bbb------------------------------> "<<bbb<<std::endl;
std::cout<< "BUFFER  ::"<<buffer<<std::endl;
//outdata<<buffer;
//cvsdata<<buffer;
filePutContents("/home/doga18/Desktop/prevla_leap_doga/catkin_ws/log/palmer.csv",buffer2,true);
    return palm_centre;
}

/*!
 * \brief Creates a visualization of an entire hand from he wrist up.
 * 
 * Using the given information calls out different functions to create a visualization of
 * a detected hand for displaying in Rviz.
 * 
 * \param marker_array  An array into which all created markers will be added
 * \param human         Pointer to a received Human.msg
 * \param hand          A hand.msg from which the hand visualization will be created.
 * \param hand_ns       Used to create a unique namespace
 * \param hand_id       A unique id to the create markers
 */

void createVisualization(visualization_msgs::MarkerArray* marker_array, const leap_motion::Human::ConstPtr& human,
    leap_motion::Hand hand, std::string hand_ns, uint8_t hand_id){

    marker_array->markers.push_back(createPalmPosition(human, hand_ns, 55, hand.palm_center));
    marker_array->markers.push_back(createHandOutline(human, hand_ns, hand_id, hand) );
    printf("[DOGA_INFO]     marker_array         --> %f\n",    marker_array);

    leap_motion::Finger finger;
    for(unsigned int j = 0; j < hand.finger_list.size(); j++)
    {
        finger = hand.finger_list[j];
        std::string ns_finger = fingerNames[finger.type];
        unsigned int id_offset = finger.bone_list.size();

        leap_motion::Bone bone;

        for(unsigned int k = 1; k < finger.bone_list.size(); k++)
        {
            bone = finger.bone_list[k];
            marker_array->markers.push_back(createFingerLines(human, hand_ns, ns_finger, k, bone));
            marker_array->markers.push_back(createJointMarker(human, hand_ns, ns_finger, k + id_offset, bone.bone_start));
               

            
            // The circle at the very bottom of the pinky
            if(finger.type == Leap::Finger::Type::TYPE_PINKY)
            {
                leap_motion::Bone temp_bone = finger.bone_list[0];
                marker_array->markers.push_back(createJointMarker(human, hand_ns, ns_finger,
                    k + id_offset+1, temp_bone.bone_start));   


            }
            // Fingertip circles
            if(k == Leap::Bone::Type::TYPE_DISTAL)
            {
                marker_array->markers.push_back(createJointMarker(human, hand_ns, ns_finger,
                    k + id_offset + 2, bone.bone_end));

            }

        }
    }
}

/*!
 * \brief Called when a new Human.msg is received.
 * 
 * \param human    Pointer to thr received Human.msg
 */
void frameCallback(const leap_motion::Human::ConstPtr& human){

    visualization_msgs::MarkerArray marker_array;
    leap_motion::Hand hand;

    if( human -> right_hand.is_present )
    {
        hand = human -> right_hand;
        createVisualization(&marker_array, human, hand, "Right", 0);
    }
    
    if( human -> left_hand.is_present )
    {
        hand = human -> left_hand;
        createVisualization(&marker_array, human, hand, "Left", 1);

    }
    
    marker_pub->publish(marker_array);


}

int main(int argc, char** argv) {

////////////////////////////////////////////////////////////////////////
if (true) {
  std::string line; std::string line2;  int lines = 0;int lines2 = 0;  std::string filename; std::string filename2;  ifstream file;ifstream file2;
  filename="/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/log/radar_data_doga.csv";file.open(filename);
  //filename2="/home/doga18/Desktop/prevla_leap_doga/catkin_ws/log/palmer.csv";file2.open(filename2);
  while (!file.eof()){getline(file, line);std::cout << line <<std:: endl;lines++;}
  //while (!file2.eof()){getline(file2, line2);std::cout << line2 <<std:: endl;lines2++;}
  file.close();  file2.close();  std::cout << "Total Lines 1-2: " << lines <<"-"<<lines2 << std::endl;
  pntind=lines-1;plmind=pntind/23;  //pntind2=int(pntind/22); 

  printf("pntind  : %d\n",pntind);
  printf("pntind2 : %d\n",pntind2);
  printf("plmind  : %d\n",plmind);
}
("yoo");
////////////////////////////////////////////////////////////////////////








    ros::init(argc, argv, "leap_motion");
    ros::NodeHandle nh("leap_motion");
    bool enable_filter;

    nh.getParam("/enable_filter", enable_filter);
    ros::Subscriber human_sub;

    human_sub = nh.subscribe<leap_motion::Human>("leap_device", 1, frameCallback);
    if(enable_filter)
    {
        human_sub = nh.subscribe<leap_motion::Human>("leap_filtered", 1, frameCallback);
    }

    ROS_INFO("enable_filter: %s", enable_filter ? "true" : "false");
    
    ros::Publisher m_pub = nh.advertise<visualization_msgs::MarkerArray>("visualization_marker_array", 1);
    marker_pub = &m_pub;

    ros::spin();
    return 0;
}

