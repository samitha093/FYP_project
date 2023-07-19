package com.example.predictionapp;

import android.annotation.SuppressLint;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import android.Manifest;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import org.java_websocket.handshake.ServerHandshake;
import org.tensorflow.lite.Interpreter;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.URI;
import java.net.URISyntaxException;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Set;
import java.util.UUID;

import android.util.Log;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;


public class MainActivity extends AppCompatActivity {
    private static final int REQUEST_ENABLE_BT = 1;
    Interpreter localTfliteModel;
    Interpreter receivedTfliteModel;
    float localModelAccuracy = 0;
    float receivedModelAccuracy = 0;
    int[][] dataArray;
    Button buttonBT;
    FileTransferWebSocketClient webSocketClient;
    private EditText etName, etGender, etNIC, etCity;
    private Button sendMsgButton;
    private TextView dataTextView;
    private TextView receivedDataTextView;
    private Handler handler;
    private BluetoothReceiver bluetoothReceiver;
    private BluetoothAdapter bluetoothAdapter;
    private BluetoothDevice selectedDevice;

    public static void copyModelToInternalStorage(Context context, String modelName) throws IOException {
        InputStream inputStream = context.getAssets().open(modelName);

        File modelFile = new File("/data/data/com.example.predictionapp/files", modelName);
        OutputStream outputStream = new FileOutputStream(modelFile);

        byte[] buffer = new byte[1024];
        int length;
        while ((length = inputStream.read(buffer)) > 0) {
            outputStream.write(buffer, 0, length);
        }
        Log.i("local model", "is transferred successfully");
        outputStream.flush();
        outputStream.close();
        inputStream.close();
    }

    public static int[] argmax(float[][] array, int axis) {
        int[] result = new int[array.length];
        for (int i = 0; i < array.length; i++) {
            float max = array[i][0];
            int index = 0;
            for (int j = 1; j < array[i].length; j++) {
                if (array[i][j] > max) {
                    max = array[i][j];
                    index = j;
                }
            }
            result[i] = index;
        }
        return result;
    }

    @SuppressLint("MissingInflatedId")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Get references to UI elements
        etName = findViewById(R.id.editTextName);
        etGender = findViewById(R.id.editTextGender);
        etNIC = findViewById(R.id.editTextNIC);
        etCity = findViewById(R.id.editTextCity);

        Button btnSave = findViewById(R.id.buttonSave);
        File csvFile = new File(getFilesDir(), "user_data.csv");
        btnSave.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                saveForm();
            }
        });
        // Initialize the WebSocket client
        Context context = getApplicationContext();
        webSocketClient = new FileTransferWebSocketClient(context);


        // Connect to the WebSocket server
        webSocketClient.connectWebSocket();

        // Check if the ACCESS_FINE_LOCATION permission is granted
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            // Permission is not granted, request it
            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.ACCESS_FINE_LOCATION},
                    REQUEST_ENABLE_BT);
        }

        // Register for broadcasts when a device is discovered.
        IntentFilter filter = new IntentFilter(BluetoothDevice.ACTION_FOUND);

        bluetoothReceiver = new BluetoothReceiver();
        bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        //registerReceiver(receiver, filter);
        try {
            copyModelToInternalStorage(this, "model.tflite");
            // Success: Model copied to internal storage
        } catch (IOException e) {
            e.printStackTrace();
            // Error: Failed to copy model
        }


    }

    @Override
    protected void onResume() {
        super.onResume();
        IntentFilter filter = new IntentFilter(BluetoothAdapter.ACTION_STATE_CHANGED);
        registerReceiver(bluetoothReceiver, filter);
        //handleBluetoothActions();
    }

    @Override
    protected void onPause() {
        super.onPause();
        unregisterReceiver(bluetoothReceiver);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        // File csvFile = new File(getFilesDir(), "user_data.csv");
        if (requestCode == REQUEST_ENABLE_BT) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                //handleBluetoothActions();
            } else {
                // Bluetooth permission denied, handle accordingly (e.g., show a message, disable Bluetooth feature, etc.)
                //Toast.makeText(MainActivity.this, "Bluetooth permission denied", Toast.LENGTH_SHORT).show();
            }
        }
    }

    @Override
    protected void onDestroy() {
        webSocketClient.disconnectWebSocket();
        super.onDestroy();

    }

    private void saveForm() {

        String name = etName.getText().toString();
        String gender = etGender.getText().toString();
        String NIC = etNIC.getText().toString();
        String city = etCity.getText().toString();

        String userData = name + "," + gender + "," + NIC + "," + city + "\n";
        // Create the file name

        String userDataCsv = "user_data.csv";

        String existingFormData = readFormData();

        if (existingFormData != null && existingFormData.contains(userData)) {
            //Check whether an user exists or not
            Toast.makeText(getApplicationContext(), "This user has been already added", Toast.LENGTH_SHORT).show();

        } else {
            try {
                FileOutputStream fileOutputStream = openFileOutput(userDataCsv, Context.MODE_APPEND);
                fileOutputStream.write(userData.getBytes());
                fileOutputStream.close();
                Calendar calendar = Calendar.getInstance();
                loadModel("model");
                int currentMonth = calendar.get(Calendar.MONTH) + 1;
                predict(currentMonth, Integer.parseInt(gender));
                // Clear the text boxes
                etName.setText("");
                etGender.setText("");
                etNIC.setText("");
                etCity.setText("");

                Toast.makeText(getApplicationContext(), "A new user is added ", Toast.LENGTH_SHORT).show();

            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    private String readFormData() {
        try {
            FileInputStream fis = openFileInput("user_data.csv");
            InputStreamReader isr = new InputStreamReader(fis);
            BufferedReader br = new BufferedReader(isr);

            StringBuilder stringBuilder = new StringBuilder();
            String line;

            while ((line = br.readLine()) != null) {
                stringBuilder.append(line).append("\n");
            }
            br.close();
            return stringBuilder.toString();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return null;
    }

    private void loadModel(String fileName) {
        try {
            if (fileName == "model") {
                localTfliteModel = new Interpreter(loadFile(fileName));
                Log.i(" Prediction App", fileName + " is loaded success fully");
            } else if (fileName == "receivedModel") {
                receivedTfliteModel = new Interpreter(loadFile(fileName));
                Log.i(" Prediction App", fileName + " is  loaded success fully");

            } else {
                Log.i(" Prediction App", fileName + " is  not loaded");

            }

        } catch (Exception ex) {
            ex.printStackTrace();
            Log.i("Prediction App", "Error");
            Log.i("Prediction App", ex.toString());
        }
    }

    private MappedByteBuffer loadFile(String fileName) throws IOException {
        // Get the path to the model file in the internal storage directory
        File directory = new File("/data/data/com.example.predictionapp/files");
        File modelFile = new File(directory, fileName + ".tflite");

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

    private void predict(int month, int gender) {
        float[] x_data = {month, gender};

        float[][] x_np = new float[1][2];
        x_np[0] = x_data;
        x_np[0][0] /= 12;
        x_np[0][1] /= 12;

        float[][] output = new float[1][7];
        localTfliteModel.run(x_np, output);
        int[] y_pred_model_1 = argmax(output, 1);

        TextView txtPredictItem = findViewById(R.id.textItem);

        for (int i = 0; i < y_pred_model_1.length; i++) {
            Log.i(" Prediction App ", "Prediction results: " + String.valueOf(y_pred_model_1[i]));
            txtPredictItem.setText("Predicted Item: " + String.valueOf(y_pred_model_1[i]));
        }
    }


}