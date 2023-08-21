package com.example.predictionapp;

import static com.example.predictionapp.SignUpActivity.argmax;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.res.AssetManager;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import org.tensorflow.lite.Interpreter;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.Socket;
import java.net.URL;
import java.net.UnknownHostException;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.util.ArrayList;
import java.util.List;

public class GetStartedActivity extends AppCompatActivity {
    Interpreter localTfliteModel;
    Interpreter receivedTfliteModel;
    float localModelAccuracy=0;
    float receivedModelAccuracy=0;
    int[][] dataArray;
    private static final String SERVER_ADDRESS = "192.168.8.198";
    private static final int SERVER_PORT = 8000;
    //private TextView lblAccount = findViewById(R.id.lblAccount);
    @Override
    protected void onCreate(Bundle savedInstanceState) {


        super.onCreate(savedInstanceState);
        setContentView(R.layout.get_started);

        new Thread(new Runnable() {
            @Override
            public void run() {

              copyAssetToInternalStorage(getApplicationContext(), "received_checkout_data.txt", "received_checkout_data.txt");
              convertTxtToCsv(getApplicationContext());
              readCsv("v");
              checkAndInitializeLocalModel();
               //backroundProcess("V");
            }
        }).start();


        Button loginButton = findViewById(R.id.btnLogin);
        Button signUpButton = findViewById(R.id.btnSignUp);

        SharedPreferences sharedPreferences = getSharedPreferences("user_prefs", MODE_PRIVATE);
        boolean isLoggedIn = sharedPreferences.getBoolean("isLoggedIn", false);

        if (isLoggedIn) {
            // User is logged in, navigate to the home activity
            Intent intent = new Intent(this, ProductPreviewActivity.class);
            startActivity(intent);
            //finish(); // Optional, to prevent going back to the MainActivity
        }

        loginButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(GetStartedActivity.this, LoginActivity.class);
                startActivity(intent);
            }
        });

        signUpButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(GetStartedActivity.this, SignUpActivity.class);
                startActivity(intent);
            }
        });
        if (doesUserDataExist()) {
            signUpButton.setVisibility(View.GONE); // Hide the button
            //lblAccount.setVisibility(View.GONE);
        } else {
            signUpButton.setVisibility(View.VISIBLE); // Show the button
            //lblAccount.setVisibility(View.VISIBLE);
        }
    }

    private boolean doesUserDataExist() {
        String fileName = "user_data.json";
        File file = new File(getApplicationContext().getFilesDir(), fileName);
        return file.exists();
    }
    //---------------------model replacing --------------------
    private void backroundProcess(String v)
    {
        //two modes of model accuray 1.localModel 2.receivedModel

        //load local model
        loadModel("localModel");
        //load csv file
        readCsv("V");
        //get model accuray
        localModelAccuracy =  modelAccuracy("localModel");
        String fileName="receivedModel";
        //loop process untill received model accuracy greater than local model accuracy
        while (true){
            //connect to socket and get url
            Log.i("MyApp", "Socket conneting...");

            String fileUrl =  socketConnect("V");

            if(fileUrl !="ERROR"){
                Log.i("MyApp", "Socket connected.");
                //download the model and save in internal memory
                saveReceivedModel(fileUrl,fileName);
                //load received model
                loadModel(fileName);
                //get model accuray
                receivedModelAccuracy =  modelAccuracy(fileName);
                if(localModelAccuracy  < receivedModelAccuracy){
                    //now we have higher received model accuracy
                    Log.i("MyApp", "Received model accuracy higher than local model accuracy. Loop stop");
                    break;
                }
                else{
                    Log.i("MyApp", "Received model accuracy not higher than local model accuracy. Loop continue");
                }

                //delete received model
                deleteFiles(fileName);
            }
            else{
                Log.i("MyApp", "Socket ERROR");
                Log.i("MyApp", "Reconnect");
            }

        }

        //delete current local model
        deleteFiles("localModel");
        //rename recieved model as local model
        renameModel(fileName,"localModel");
        Log.i("MyApp", "Successfully updated model saved to internal storage");

    }
    private void loadModel(String fileName){
        try {
            if(fileName=="localModel")
            {
                localTfliteModel = new Interpreter(loadFile(fileName));
                Log.i("MyApp", fileName+" load success fully");
            }
            else if(fileName=="receivedModel") {
                receivedTfliteModel = new Interpreter(loadFile(fileName));
                Log.i("MyApp", fileName+" load success fully");

            }
            else{
                Log.i("MyApp", fileName+" not loaded");

            }

        }catch (Exception ex){
            ex.printStackTrace();
            Log.i("MyApp", "Error");
            Log.i("MyApp", ex.toString());
        }
    }
    private MappedByteBuffer loadFile(String fileName) throws IOException {
        // Get the path to the model file in the internal storage directory
        File directory = new File(getFilesDir(), "models");
        File modelFile = new File(directory, fileName+".tflite");

        // Open the model file as a FileInputStream
        FileInputStream inputStream = new FileInputStream(modelFile);

        // Get a FileChannel from the FileInputStream
        FileChannel fileChannel = inputStream.getChannel();

        // Get the start offset and declared length of the model file
        long startOffset = 0;
        long declareLength = modelFile.length();

        // Map the model file to a MappedByteBuffer
        MappedByteBuffer mappedByteBuffer = fileChannel.map(FileChannel.MapMode.READ_ONLY, startOffset, declareLength);

        // Close the input stream and file channel
        inputStream.close();
        fileChannel.close();

        // Return the MappedByteBuffer
        return mappedByteBuffer;
    }
    //read csv file for asset
    private void readCsv(String v){
        // Load the CSV file from the assets folder
        //String fileName = "dataset.csv";
        //String[] data = loadDataFromAsset(this, fileName);
        String fileName = "converted_checkout_data.csv";
        String[] data = loadCheckoutCsv(this, fileName);
        Log.i("MyApp", "data set Loaded");
        // Preview the data in the console


        // Split the first row into column names (if needed)
        String[] columnNames = data[0].split(",");

        // Initialize the intData array
        int[][] intData = new int[data.length-1][columnNames.length];

        // Convert the data into integers and store in the intData array
        for (int i = 1; i < data.length; i++) {
            String[] rowData = data[i].split(",");
            for (int j = 0; j < columnNames.length; j++) {
                intData[i-1][j] = Integer.parseInt(rowData[j]);
            }
        }
        Log.i("MyApp", "Save to Global array");
        dataArray =intData;
    }

    private String[] loadDataFromAsset(Context context, String fileName) {
        AssetManager assetManager = context.getAssets();
        StringBuilder stringBuilder = new StringBuilder();

        try {
            // Open the CSV file as an InputStream and read its contents
            InputStream inputStream = assetManager.open(fileName);
            BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));

            String line;
            while ((line = bufferedReader.readLine()) != null) {
                stringBuilder.append(line).append("\n");
            }

            bufferedReader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Convert the CSV data to an array of Strings
        return stringBuilder.toString().split("\n");
    }
    private String[] loadCheckoutCsv(Context context, String fileName) {
        File file = new File(context.getFilesDir(), fileName);
        StringBuilder stringBuilder = new StringBuilder();

        try {
            // Open the CSV file as a FileInputStream and read its contents
            FileInputStream fileInputStream = new FileInputStream(file);
            BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(fileInputStream));

            String line;
            while ((line = bufferedReader.readLine()) != null) {
                stringBuilder.append(line).append("\n");
            }

            bufferedReader.close();
            fileInputStream.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Convert the CSV data to an array of Strings
        return stringBuilder.toString().split("\n");
    }
    private float modelAccuracy(String accuracyMode){
        int[][] data= dataArray;

        float[][] input_values = new float[data.length][2];
        int[][] realOutput = new int[data.length][1];

        for (int i = 0; i < data.length; i++) {
            input_values[i][0] = (float) data[i][0];
            input_values[i][1] = (float) data[i][1];
            realOutput[i][0] = data[i][2];
        }

// define input and output arrays
        float[][] x_np = new float[input_values.length][2];
        float[][] output = new float[1][9];

        int correctPredictions = 0;

// loop over input values
        for (int i = 0; i < input_values.length; i++) {
            // set input values
            x_np[i] = input_values[i];
            x_np[i][0] /= 12;
            x_np[i][1] /= 12;

            // run prediction
            if(accuracyMode=="localModel"){
                localTfliteModel.run(x_np[i], output);
            }

            else if(accuracyMode=="receivedModel"){
                receivedTfliteModel.run(x_np[i], output);
            }
            // get predicted label for this input value
            int y_pred = argmax(output, 1)[0];
            int value = realOutput[i][0];

            if (y_pred == value) {
                correctPredictions++;
            }
            // print the predicted label
//            Log.i("MyApp", "Prediction for input " + i + ": " + y_pred);
//            Log.i("MyApp", "Real value for input " + i + ": " + value);
        }

        float accuracy = ((float) correctPredictions / input_values.length) * 100;
        Log.i("MyApp", accuracyMode+" Accuracy: " + accuracy + "%");
        return accuracy;

    }

    //close model accuracy

    //socket connect
    private String socketConnect(String v) {
        try {
            //create socket and connect to server
            Socket socket = new Socket(SERVER_ADDRESS, SERVER_PORT);
            System.out.println("Connected to server.");
            Log.i("Socket", "Connected to server.");
            //data recive untill recive  new line caractor
            BufferedReader BReader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            //print data recived for reader variable
            String MyUrl = BReader.readLine();
            System.out.println("Received data : " + MyUrl);
            Log.i("Socket", "received address : " + MyUrl);
            //socket close
            socket.close();
            //save incoming model
            Log.i("Socket", "Socket closed : " + MyUrl);
            return MyUrl;
        }
        catch (UnknownHostException e) {
            Log.i("Socket", "ERROR: Server not found.");
            System.err.println("ERROR: Server not found.");
        }
        catch (IOException e) {
            e.printStackTrace();
        }
        return "ERROR";
    }

    private void saveReceivedModel(String MyUrl,String fileName){
        try {
            Log.i("MyApp", "Try ");

            // MyUrl = "http://localhost:5000/download?ID=123";
            URL url = new URL(MyUrl);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            Log.i("MyApp", "Call Request ");

            if (conn.getResponseCode() == HttpURLConnection.HTTP_OK) {
                Log.i("MyApp", "Accept the Request ");
                Log.i("MyApp", "Input Stream");

                InputStream inputStream = conn.getInputStream();

                // Get the path to the internal storage directory
                File directory = new File(getFilesDir(), "models");
                directory.mkdirs();
//                Log.i("Socket", "models dir");

                // Create a new file in the internal storage directory and copy the model data to it
                File modelFile = new File(directory, fileName+".tflite");
//                File modelFile = new File(directory, "model.tflite");

                OutputStream outputStream = new FileOutputStream(modelFile);

//                    FileOutputStream outputStream = new FileOutputStream(fileName);
                byte[] buffer = new byte[1024];
                int bytesRead = -1;
                Log.i("MyApp", "read....");
                while ((bytesRead = inputStream.read(buffer)) != -1) {
                    outputStream.write(buffer, 0, bytesRead);
                    Log.i("MyApp", "Writing....");
                }

                outputStream.close();
                inputStream.close();
                Log.i("MyApp", "Successfully save to internal storage "+fileName);
            }
            else {
                Log.i("MyApp", "Failed to download file. Response code: "+fileName +" : " + conn.getResponseCode());
                System.out.println("Failed to download file. Response code: " + conn.getResponseCode());
            }
        } catch (Exception e)
        {
            e.printStackTrace();
        }
    }

    private void deleteFiles(String deleteFileName) {
        File receivedModelFile = new File(getFilesDir() + "/models/"+deleteFileName+".tflite");
        if (receivedModelFile.exists()) {
            if (receivedModelFile.delete()) {
                Log.i("MyApp", deleteFileName+" deleted successfully.");
            } else {
                Log.i("MyApp", deleteFileName+" delete failed.");
            }
        } else {
            Log.i("MyApp", deleteFileName+" not found.");
        }

    }

    //model rename and delete files
    private void renameModel(String originalName,String rename){

        File modelFile = new File(getFilesDir() + "/models/"+originalName+".tflite");
        File newModelFile = new File(getFilesDir() + "/models/"+rename+".tflite");
        if(modelFile.exists()) {
            if(modelFile.renameTo(newModelFile)) {
                Log.i("MyApp", "File "+originalName +" renamed as "+rename+" successfully.");
            } else {
                Log.i("MyApp", originalName+" rename failed.");
            }
        } else {
            Log.i("MyApp", originalName+" not found.");
        }
    }

    //for model initializing ------ test-------
    //COPY MODEL FROM ASSESTS TO INTERNAL STORAGE
    private void copyToInternalStorage(String v){
        Log.i("MyApp", "copyToInternalStorage function start");
        try {
            // Open the model file from the assets folder
            InputStream inputStream = getAssets().open("model.tflite");
            Log.i("MyApp", "Read from assets");

            // Get the path to the internal storage directory
            File directory = new File(getFilesDir(), "models");
            directory.mkdirs();

            // Create a new file in the internal storage directory and copy the model data to it
            File modelFile = new File(directory, "localModel.tflite");
            OutputStream outputStream = new FileOutputStream(modelFile);
            byte[] buffer = new byte[1024];
            int length;
            while ((length = inputStream.read(buffer)) > 0) {
                outputStream.write(buffer, 0, length);
            }
            outputStream.close();
            inputStream.close();
            Log.i("MyApp", "Save to internal storage");

            // Now the model file is copied to the internal storage directory and can be accessed from there
            //check existency
            File directory1 = new File(getFilesDir(), "models");
            File modelFile1 = new File(directory1, "localModel.tflite");

            if (modelFile1.exists()) {
                Log.i("MyApp", "Successfully load from internal storage");

                // The model file was successfully copied to the internal storage directory
                // You can now load the model from this file using the code I provided in my previous response
            } else {
                Log.i("MyApp", "Failed to load from internal storage");
                // The model file was not copied to the internal storage directory
                // Handle the error
            }

        } catch (IOException e) {
            // Handle the error
            Log.i("MyApp", "Failed to save internal storage");
            Log.i("MyApp", e.toString());
        }

    }
    public static void convertTxtToCsv(Context context) {
        try {
            String fileName = "received_checkout_data.txt";
            File inputFile = new File(context.getFilesDir(), fileName);
            File outputFile = new File(context.getFilesDir(), "converted_checkout_data.csv");

            BufferedReader reader = new BufferedReader(new FileReader(inputFile));
            BufferedWriter writer = new BufferedWriter(new FileWriter(outputFile));

            List<String> last250Lines = new ArrayList<>();
            String line;
            while ((line = reader.readLine()) != null) {
                last250Lines.add(line);
                if (last250Lines.size() > 250) {
                    last250Lines.remove(0); // Remove the oldest line
                }
            }

            for (String processedLine : last250Lines) {
                // Remove brackets and extra spaces
                processedLine = processedLine.replaceAll("\\[|\\]|\\s", "");
                writer.write(processedLine);
                writer.newLine();
            }

            reader.close();
            writer.close();

            System.out.println("Conversion completed: " + outputFile.getAbsolutePath());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    //-------------this is for testing-----------
    public static void copyAssetToInternalStorage(Context context, String assetFileName, String internalFileName) {
        try {
            InputStream inputStream = context.getAssets().open(assetFileName);
            File internalFile = new File(context.getFilesDir(), internalFileName);
            OutputStream outputStream = new FileOutputStream(internalFile);

            byte[] buffer = new byte[1024];
            int length;
            while ((length = inputStream.read(buffer)) > 0) {
                outputStream.write(buffer, 0, length);
            }

            outputStream.flush();
            outputStream.close();
            inputStream.close();

            System.out.println("File copied to internal storage: " + internalFile.getAbsolutePath());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // checking for availabilty of local model in internal stroage
    private boolean isLocalModelFileAvailable() {
        File directory = new File(getFilesDir(), "models");
        File modelFile = new File(directory, "localModel.tflite");
        return modelFile.exists();
    }
    //initialize the local model
    private void initializeLocalModelIfNeeded() {
        if (!isLocalModelFileAvailable()) {
            copyToInternalStorage("model.tflite");
        }
    }

    // check and initialize local model
    private void checkAndInitializeLocalModel() {
        if (!isLocalModelFileAvailable()) {
            Log.i("LOCAL MODEL","NEW LOCAL MODEL INITIALIZING STARTING...");
            initializeLocalModelIfNeeded();
            Log.i("LOCAL MODEL","NEW LOCAL MODEL IS INITIALIZED SUCCESSFULLY");

        }
        else{
            Log.i("LOCAL MODEL","ALREADY A LOCAL MODEL IS THERE");
        }
    }
}
