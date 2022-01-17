package com.example.rosapp;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;

import io.github.controlwear.virtual.joystick.android.JoystickView;

public class MenuActivity extends AppCompatActivity {

    // Botones para follow path y record path, respectivamente
    Button button_executePath, button_recordPath, button_wait, button_followPerson, button_goHome, button_setHome, button_exit, button_forgetPath, button_joystick_tp;
    TextView mode;
    int i = 0;
    String IP_host = "192.168.1.46";
    int IP_port = 6000;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_menu);

        // Me guardo la IP y el puerto que he introducido en MainActivity
        Intent intent = getIntent();
        Bundle extras = intent.getExtras();
        String IP_host = extras.getString("EXTRA_IP");
        String IP_port_tmp = extras.getString("EXTRA_PORT");
        IP_port = Integer.parseInt(IP_port_tmp);

//        TextView textView = findViewById(R.id.show_main);
//        textView.setText(IP_host);

        button_executePath = (Button) findViewById(R.id.button_execute);
        button_recordPath = (Button) findViewById(R.id.button_record);
        button_wait = (Button) findViewById(R.id.button_w);
        button_exit = (Button) findViewById(R.id.button_exit);
        button_followPerson = (Button) findViewById(R.id.button_follow);
        button_forgetPath = (Button) findViewById(R.id.button_forget);
        button_goHome = (Button) findViewById(R.id.button_goHome);
        button_setHome = (Button) findViewById(R.id.button_setHome);
        button_joystick_tp = (Button) findViewById(R.id.button_teleop);

        mode = (TextView) findViewById(R.id.text_mode);

        joystick_onMove();
        button_recordPath_onClick();
        button_executePath_onClick();
        button_wait_onClick();
        button_exit_onClick();
        button_forgetPath_onClick();
        button_followPerson_onClick();
        button_goHome_onClick();
        button_setHome_onClick();
        button_joystickTp_onClick();

    }

    public void joystick_onMove() {
        JoystickView joystick = (JoystickView) findViewById(R.id.joystickView);
        joystick.setOnMoveListener(new JoystickView.OnMoveListener() {
            @Override
            public void onMove(int angle, int strength) {
                angle -= 90;
                if (angle < 0){ angle += 360; }

                String message = "j";
                String ang = "000";
                String vel = "00";

                if (angle < 10){
                    ang = "00" + String.valueOf(angle);
                }else if (angle < 100){
                    ang = "0" + String.valueOf(angle);
                }else{
                    ang = String.valueOf(angle);
                }

                if (strength < 10){
                    vel = "0" + String.valueOf(strength);
                }else if (strength == 100) {
                    vel = "99";
                }else{
                    vel = String.valueOf(strength);
                }

                message = message + ang + vel;

//                System.out.println(message);

                MenuActivity.BackGroundTask b11 = new MenuActivity.BackGroundTask();
                b11.execute(message);
            }
        });
    }

    public void button_recordPath_onClick() {

        button_recordPath.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view){
                String message = "r00000";
                MenuActivity.BackGroundTask b2 = new MenuActivity.BackGroundTask();
                b2.execute(message);
            }
        });
    }

    public void button_executePath_onClick() {

        button_executePath.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view){
                String message = "p00000";
                MenuActivity.BackGroundTask b3 = new MenuActivity.BackGroundTask();
                b3.execute(message);
            }
        });
    }

    public void button_wait_onClick() {

        button_wait.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view){
                String message = "w00000";
                MenuActivity.BackGroundTask b4 = new MenuActivity.BackGroundTask();
                b4.execute(message);
            }
        });
    }

    public void button_exit_onClick() {

        button_exit.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view){
                String message = "e00000";
                MenuActivity.BackGroundTask b5 = new MenuActivity.BackGroundTask();
                b5.execute(message);
            }
        });
    }

    public void button_goHome_onClick() {

        button_goHome.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view){
                String message = "h00000";
                MenuActivity.BackGroundTask b6 = new MenuActivity.BackGroundTask();
                b6.execute(message);
            }
        });
    }

    public void button_setHome_onClick() {

        button_setHome.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view){
                String message = "s00000";
                MenuActivity.BackGroundTask b7 = new MenuActivity.BackGroundTask();
                b7.execute(message);
            }
        });
    }

    public void button_followPerson_onClick() {

        button_followPerson.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view){
                String message = "f00000";
                MenuActivity.BackGroundTask b8 = new MenuActivity.BackGroundTask();
                b8.execute(message);
            }
        });
    }

    public void button_forgetPath_onClick() {

        button_forgetPath.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view){
                String message = "n00000";
                MenuActivity.BackGroundTask b9 = new MenuActivity.BackGroundTask();
                b9.execute(message);
            }
        });
    }

    public void button_joystickTp_onClick() {

        button_joystick_tp.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view){
                String message = "t00000";
                MenuActivity.BackGroundTask b10 = new MenuActivity.BackGroundTask();
                b10.execute(message);
            }
        });
    }

    class BackGroundTask extends AsyncTask<String, Void, Void> {

        Handler h = new Handler();
        @Override
        protected Void doInBackground(String... voids) {
            try {
                String message = voids[0];
                String msg = "MODE: ";

                switch (message){
                    case "w00000":
                        msg += getResources().getString(R.string.wait_bt_name);
                        break;
                    case "p00000":
                        msg += getResources().getString(R.string.path_bt_name);
                        break;
                    case "r00000":
                        msg += getResources().getString(R.string.record_bt_name);
                        break;
                    case "s00000":
                        msg += getResources().getString(R.string.wait_bt_name);
                        break;
                    case "f00000":
                        msg += getResources().getString(R.string.follow_bt_name);
                        break;
                    case "n00000":
                        msg += getResources().getString(R.string.wait_bt_name);
                        break;
                    case "h00000":
                        msg += "Home";
                        break;
                    case "t00000":
                        msg += "Joystick Control";
                        break;
                }

                if(MainActivity.s == null){
                    MainActivity.s = new Socket(IP_host, IP_port);
                    MainActivity.writer = new PrintWriter(MainActivity.s.getOutputStream());
                    Log.i("i", "CONNECTED");
                }

                MainActivity.writer.write(message);
                MainActivity.writer.flush();

//                byte[] messageByte = new byte[1000];
//                boolean end = false;
//                String data = "";
////                while(!end){
//                int bytesRead = MainActivity.input.read(messageByte);
//                System.out.println(bytesRead);
//                data += new String(messageByte, 0, bytesRead);
////                    if (data.length() == 2) {
////                        end = true;
////                    }
////                }
//                System.out.println(data);

                String finalMsg = msg;
                h.post(new Runnable() {
                    @Override
                    public void run() {
                        mode.setText(finalMsg);
                    }
                });
            }
            catch (IOException e) {
                e.printStackTrace();
            }
            return null;
        }
    }


}