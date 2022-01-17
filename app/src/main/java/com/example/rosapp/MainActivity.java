package com.example.rosapp;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import androidx.appcompat.app.AppCompatActivity;

import java.io.BufferedInputStream;
import java.io.DataInputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.Reader;
import java.net.Socket;


public class MainActivity extends AppCompatActivity {

    public static final String EXTRA_SOCKET = "com.example.rosapp.MESSAGE";

    Button button_main;
    public static Socket s;
    public static PrintWriter writer;
    public static DataInputStream input;
    String host_IP = "192.168.1.1";
    String host_PORT = "5000";   // 5000 is default port

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        button_main = (Button) findViewById(R.id.button_main);

        onBtnClick();
    }

    public void onBtnClick() {

//        Handler h = new Handler();
        button_main.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view){
                BackGroundTask b1 = new BackGroundTask();
                b1.execute("hola");
            }
        });
    }


    class BackGroundTask extends AsyncTask<String, Void, Void> {

        Handler h = new Handler();

        @Override
        protected Void doInBackground(String... voids) {
            try {
                String message = voids[0];

                EditText text_IP = (EditText) findViewById(R.id.enter_IP);
                EditText text_PORT = (EditText) findViewById(R.id.enter_PORT);
                host_IP = text_IP.getText().toString();
                host_PORT = text_PORT.getText().toString();
                int n_PORT = Integer.parseInt(host_PORT);

                if (s == null) {
                    //change it to your IP
                    s = new Socket(host_IP, n_PORT);
//                    SocketHandler.setSocket(s);       // Para compartir el socket con todas las actividades
                    writer = new PrintWriter(s.getOutputStream());
                    input = new DataInputStream(s.getInputStream());
                    Log.i("i", "CONNECTED");
                    writer.write("C00000");
                    writer.flush();
                }
//                byte[] messageByte = new byte[1000];
//                boolean end = false;
//                String data = "";
//                int bytesRead = MainActivity.input.read(messageByte);
//                System.out.println(bytesRead);
//                data += new String(messageByte, 0, bytesRead);

                Intent intent = new Intent(MainActivity.this, MenuActivity.class);
                Bundle extras = new Bundle();
                extras.putString("EXTRA_IP", host_IP);
                extras.putString("EXTRA_PORT", host_PORT);
                intent.putExtras(extras);
                startActivity(intent);

            } catch (IOException e) {
                e.printStackTrace();
            }
            return null;
        }
    }
}
