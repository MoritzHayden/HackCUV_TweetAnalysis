package sample;
// Install the Java helper library from twilio.com/docs/libraries/java
import com.jfoenix.controls.JFXListView;
import com.jfoenix.controls.JFXSpinner;
import com.jfoenix.controls.JFXTextArea;
import com.twilio.Twilio;
import com.twilio.rest.api.v2010.account.Message;
import com.twilio.type.PhoneNumber;
import javafx.concurrent.Task;
import javafx.scene.control.TextField;
import javafx.fxml.FXML;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.Scanner;
import java.lang.Math;


public class Controller {
    // Find your Account Sid and Auth Token at twilio.com/console
    public static final String ACCOUNT_SID =
            "AC50be52a947487068848265c7a78b2441";
    public static final String AUTH_TOKEN =
            "1e5ba1b20f756f820c8de5b79e844903";

    String message1 = "";

    String textMessage = "";

    @FXML
    JFXTextArea resultset;

    @FXML
    JFXListView<String> tweets;

    @FXML
    TextField textf;

    @FXML
    JFXSpinner spinner;
    


    public void sendMessage(){
        Twilio.init(ACCOUNT_SID, AUTH_TOKEN);

        Message message = Message
                .creator(new PhoneNumber("+13072202394"), // to
                        new PhoneNumber("+13074149131"), // from
                        textMessage)
                .create();
        System.out.println(message.getSid());
    }

    public void enter_click() throws IOException {
        spinner.setVisible(true);
        message1 = textf.getText();


        ProcessBuilder builder = new ProcessBuilder("python", "/Users/trystan/IdeaProjects/HackCU/src/sample/extract_topic.py", message1);
        builder.redirectErrorStream(true);
        Process p = builder.start();
        BufferedReader r = new BufferedReader(new InputStreamReader(p.getInputStream()));
        String line;
        while(true){
            line = r.readLine();
            if(line == null){break;}
            System.out.println(line);
        }

        ProcessBuilder builder2 = new ProcessBuilder("python", "/Users/trystan/IdeaProjects/HackCU/sentiment_analysis.py");
        builder.redirectErrorStream(true);
        Process p2 = builder2.start();
        BufferedReader r2 = new BufferedReader(new InputStreamReader(p2.getInputStream()));
        String line2;
        while(true){
            line2 = r2.readLine();
            if(line2 == null){break;}
            System.out.println(line2);
        }

        //then run extract topic
        FileInputStream in2 = new FileInputStream("/Users/trystan/IdeaProjects/HackCU/result.txt");
        Scanner inStream2 = new Scanner(in2, String.valueOf(StandardCharsets.UTF_8));
        inStream2.useDelimiter("Summary: ");
        String[] results = inStream2.next().split("\n");
        String percentages = "";
        textMessage += message1 + "\n";
        for(int i = 0; i < results.length; i++){
            String j[] = results[i].split(":");
            double s = Double.parseDouble(j[1]);
            s = Math.round(s * 100.00) / 100.00;
            String returnThis = j[0] + ": " + Double.toString(s) + "%";
            percentages += returnThis + "\n";
            textMessage += returnThis + "\n";
        }
        resultset.setText(percentages);

        //delimit tweets
        String[] tweetlist = inStream2.next().split("RT");
        //tweets.getItems().addAll(tweetlist);
        for(int j = 1; j < tweetlist.length; j++){
            String s = new String(tweetlist[j]);
            tweets.getItems().add(s);
        }


        spinner.setVisible(true);
    }

    public void send_click(){
        sendMessage();
    }

    public void initialize(){
        spinner.setVisible(false);
       // sendMessage();

        resultset.setText(message1);



    }


}
