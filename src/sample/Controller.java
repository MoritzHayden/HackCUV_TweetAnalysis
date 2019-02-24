package sample;

import com.twilio.Twilio;
import com.twilio.rest.api.v2010.account.Message;
import com.twilio.type.PhoneNumber;


public class Controller {
    public static final String ACCOUNT_SID =
            "AC50be52a947487068848265c7a78b2441";
    public static final String AUTH_TOKEN =
            "1e5ba1b20f756f820c8de5b79e844903";

    public void sendMessage() {
        Twilio.init(ACCOUNT_SID, AUTH_TOKEN);

        Message message = Message
                .creator(new PhoneNumber("+13072202394"), // to
                        new PhoneNumber("+13074149131"), // from
                        "What's up homie.")
                .create();
        System.out.println(message.getSid());
    }

    public void initialize() {
        //sendMessage();
    }
}
