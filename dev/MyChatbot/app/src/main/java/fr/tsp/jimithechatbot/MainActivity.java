package fr.tsp.jimithechatbot;

import android.media.MediaPlayer;
import android.annotation.SuppressLint;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.*;
import androidx.appcompat.app.AppCompatActivity;
import fr.tsp.jimithechatbott.R;

import java.net.NetworkInterface;
import java.net.SocketException;
import java.util.Collections;
import java.util.List;
import java.util.Objects;

public class MainActivity extends AppCompatActivity {

    LinearLayout layoutList;
    EditText messageEdit;
    Button addButton;
    ViewFlipper flipper;
    LinearLayout discussionLayout;
    ImageView img_music;
    Button buttonMusic;
    MediaPlayer player;
    String macAddress;

    @SuppressLint("MissingPermission")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        macAddress = getMacAddress();
        //macAddress= "02:00:00:44:55:66:";
        System.out.println(macAddress);
        setContentView(R.layout.activity_main);

        messageEdit = findViewById(R.id.question);

        layoutList = findViewById(R.id.layout_list);
        addButton = findViewById(R.id.add_button);
        discussionLayout = findViewById(R.id.discussionScrollview);
        addButton.setOnClickListener(onClick);

        flipper = findViewById(R.id.flipper);

        buttonMusic = findViewById(R.id.buttonMusic);
        buttonMusic.setOnClickListener(onClickMusic);
        img_music = findViewById(R.id.img_music);
        img_music.setTag(R.drawable.pause);

        player = MediaPlayer.create(MainActivity.this,R.raw.music);
        // Musique libre de droit : https://audiotrimmer.com/fr/Feeling-Good
        player.setLooping(true);
        player.start();
    }

    private void addBubbleLeft(final String message) {
        LayoutInflater inflater = getLayoutInflater();
        View add_bubble_View = inflater.inflate(R.layout.bubble_left, null);
        TextView textView = add_bubble_View.findViewById(R.id.text_bubble_left);
        textView.setText(String.format("Jimi: %s", message));
        discussionLayout.addView(add_bubble_View);
    }

    private void addBubbleRight(final String message) {
        LayoutInflater inflater = getLayoutInflater();
        View add_bubble_View = inflater.inflate(R.layout.bubble_right, null);
        TextView textView = add_bubble_View.findViewById(R.id.text_bubble_right);
        textView.setText(String.format("Me: %s", message));
        discussionLayout.addView(add_bubble_View);
    }

    public static String error = "Error: Please try again";


    // On button click
    private final View.OnClickListener onClick = view -> traite();
    private final View.OnClickListener onClickMusic = view -> music();

    private void music() {
        if ((int) img_music.getTag() == R.drawable.pause) {
            img_music.setImageResource(R.drawable.play);
            img_music.setTag(R.drawable.play);
            //player.reset();
            player.pause();
        }
        else {
            img_music.setImageResource(R.drawable.pause);
            img_music.setTag(R.drawable.pause);
            player.start();
        }
    }

    private void traite() {
        String message = messageEdit.getText().toString();
        addBubbleRight(message);

        String url = "http://192.168.0.22:8080/";

        Communication conn = new Communication(url, message, macAddress);
        String result = conn.html();
        if (Objects.equals(result, error)) {
            result += "\n";
            Toast.makeText(MainActivity.this, error, Toast.LENGTH_SHORT).show();
        }
        addBubbleLeft(result);
    }

    public String getMacAddress(){
        try{
            List<NetworkInterface> networkInterfaceList = Collections.list(NetworkInterface.getNetworkInterfaces());
            String stringMac = "";
            for(NetworkInterface networkInterface : networkInterfaceList){
                if(networkInterface.getName().equalsIgnoreCase("wlon0"));
                {
                    for(int i=0;i <networkInterface.getHardwareAddress().length; i++){
                        String stringMacByte = Integer.toHexString(networkInterface.getHardwareAddress()[i]& 0xFF);
                        if(stringMacByte.length()==1){
                            stringMacByte = "0" +stringMacByte;
                        }
                        stringMac += stringMacByte.toUpperCase() + ":";
                    } break;
                }
            }
            return stringMac;
        }catch (SocketException e)
        {
            e.printStackTrace();
        }
        return  "0";
    }
}
