//package com.example.rosapp;
//
//import java.net.Socket;
//
//public class ConnectThread extends Thread{
//
//    private static ConnectThread instance;
//
//    public static ConnectThread getInstance(){
//        return (instance == null) ? instance = new ConnectThread() : instance;
//    }
//
//    private ConnectThread(){
//    }
//
//    public static Socket mSocket;
//
//    public static Socket getSocket(){
//        return mSocket;
//    }
//
//     @Override
//    public static void run(String IP_host, int IP_port) {
//        mSocket = new Socket(IP_host, IP_port);
//    }
//}
