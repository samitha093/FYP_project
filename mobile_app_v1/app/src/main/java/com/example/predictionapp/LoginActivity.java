package com.example.predictionapp;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.tensorflow.lite.Interpreter;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.util.Calendar;

public class LoginActivity extends AppCompatActivity {

    private EditText etUsername;
    private EditText etPassword;
    private Button btnLogin;
    private Button btnSignUp;

    Interpreter localTfLiteModel;
    Interpreter receivedTfLiteModel;
    TextView lblAccount;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.login_layout);

        etUsername = findViewById(R.id.etEmailUsername); // Replace with your username EditText ID
        etPassword = findViewById(R.id.etPassword); // Replace with your password EditText ID
        btnLogin = findViewById(R.id.btnLogin); // Replace with your login button ID
        btnSignUp = findViewById(R.id.btnSignUp);
        lblAccount = findViewById(R.id.lblAccount);
        btnLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Get entered username and password
                String username = etUsername.getText().toString();
                String password = etPassword.getText().toString();

                // Validate credentials
                if (isValidCredentials(username, password)) {

                    Toast.makeText(LoginActivity.this, "user is logged in successfully", Toast.LENGTH_SHORT).show();
                    // Successful login, navigate to the next activity
                    navigateToMainActivity();
                } else {
                    // Failed login, show error message
                    Toast.makeText(LoginActivity.this, "Invalid username or password", Toast.LENGTH_SHORT).show();
                    // Clear password field and request focus
                    etPassword.getText().clear();
                    etPassword.requestFocus();
                }
                // Store user data and set login state
                SharedPreferences sharedPreferences = getSharedPreferences("user_prefs", MODE_PRIVATE);
                SharedPreferences.Editor editor = sharedPreferences.edit();
                editor.putString("username", username);
                editor.putString("password",password);
                editor.putBoolean("isLoggedIn", true);
                editor.apply();

                Calendar calendar = Calendar.getInstance();
                loadModel("model");
                int currentMonth = calendar.get(Calendar.MONTH) + 1;
                //predict(currentMonth, getGender());
                savePredictedCategory(predict(currentMonth,getGender()));
            }
        });
        btnSignUp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(LoginActivity.this, SignUpActivity.class);
                startActivity(intent);
            }
        });
        if (doesUserDataExist()) {
            btnSignUp.setVisibility(View.GONE); // Hide the button
            lblAccount.setVisibility(View.GONE);
        } else {
            btnSignUp.setVisibility(View.VISIBLE);
            lblAccount.setVisibility(View.VISIBLE);// Show the button
        }

    }

    private boolean doesUserDataExist() {
        String fileName = "user_data.json";
        File file = new File(getApplicationContext().getFilesDir(), fileName);
        return file.exists();
    }

    private boolean isValidCredentials(String enteredUsername, String enteredPassword) {
        // Load stored user data (from JSON file or other storage mechanism)
        JSONArray userList = loadUserListFromJson(); // Implement this method to load user data
        Log.i("USER LIST", String.valueOf(userList));
        for (int i = 0; i < userList.length(); i++) {
            try {
                JSONObject user = userList.getJSONObject(i);
                String storedUsername = user.optString("email");
                String storedPassword = user.optString("password");

                // Compare entered credentials with stored data
                if (enteredUsername.equals(storedUsername) && enteredPassword.equals(storedPassword)) {
                    Log.i("ENTERED USER DATA", "UN: "+enteredUsername + " PW: "+ enteredPassword);
                    Log.i("STORED USER DATA", "UN: "+storedUsername + " PW: "+ storedPassword);
                    JSONObject userData = user;

                    // Launch ScanQRActivity and pass user's JSON data
                    Intent userProfileIntent = new Intent(LoginActivity.this, UserProfileActivity.class);
                    userProfileIntent.putExtra("userData", userData.toString());
                    startActivity(userProfileIntent);


                    return true; // Credentials match, grant access
                }
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }

        return false; // No match found, validation failed
    }
    private int getGender (){
        int genderNumber = 0;
        JSONArray userList = loadUserListFromJson(); // Implement this method to load user data
        Log.i("USER LIST", String.valueOf(userList));
        for (int i = 0; i < userList.length(); i++) {
            try {
                JSONObject user = userList.getJSONObject(i);
                String storedGender = user.optString("gender");
                if(storedGender == "Female"){
                    genderNumber = 0;
                }
                else {
                    genderNumber = 1;
                }
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }

        return genderNumber;
    }
    private JSONArray loadUserListFromJson() {
        JSONArray userList = new JSONArray();

        try {
            // Open the user data JSON file for reading
            FileInputStream inputStream = openFileInput("user_data.json");
            InputStreamReader inputStreamReader = new InputStreamReader(inputStream);
            BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
            String line;

            // Read the JSON data from the file line by line
            while ((line = bufferedReader.readLine()) != null) {
                try {
                    JSONObject user = new JSONObject(line);
                    userList.put(user);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }

            // Close the file streams
            bufferedReader.close();
            inputStreamReader.close();
            inputStream.close();

        } catch (IOException e) {
            e.printStackTrace();
        }

        return userList;
    }

    /*private JSONArray loadUserListFromJson() {
        JSONArray userList = new JSONArray();

        try {
            // Open the user data JSON file for reading
            FileInputStream inputStream = openFileInput("user_data.json");
            InputStreamReader inputStreamReader = new InputStreamReader(inputStream);
            BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
            StringBuilder stringBuilder = new StringBuilder();
            String line;

            // Read the JSON data from the file
            while ((line = bufferedReader.readLine()) != null) {
                stringBuilder.append(line);
            }

            // Close the file streams
            bufferedReader.close();
            inputStreamReader.close();
            inputStream.close();

            // Parse the JSON data into a JSONArray
            userList = new JSONArray(stringBuilder.toString());

        } catch (IOException | JSONException e) {
            e.printStackTrace();
        }

        return userList;
    }*/


    private void navigateToMainActivity() {
        // Replace MainActivity.class with the desired activity to navigate to
        Intent intent = new Intent(this, ProductPreviewActivity.class);
        startActivity(intent);
        finish(); // Optional: finish the LoginActivity to prevent going back
    }
    private void navigateToSignUpActivity() {
        // Replace MainActivity.class with the desired activity to navigate to
        Intent intent = new Intent(LoginActivity.this, SignUpActivity.class);
        startActivity(intent);
        finish(); // Optional: finish the LoginActivity to prevent going back
    }
    private void loadModel(String fileName) {
        try {
            if (fileName == "model") {
                localTfLiteModel = new Interpreter(loadFile(fileName));
                Log.i(" Prediction App", fileName + " is loaded success fully");
            } else if (fileName == "receivedModel") {
                receivedTfLiteModel = new Interpreter(loadFile(fileName));
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

    private void predictString(int month, int gender) {
        float[] x_data = {month, gender};

        float[][] x_np = new float[1][2];
        x_np[0] = x_data;
        x_np[0][0] /= 12;
        x_np[0][1] /= 12;

        float[][] output = new float[1][7];
        localTfLiteModel.run(x_np, output);
        int[] y_pred_model_1 = argmax(output, 1);

        //TextView txtPredictItem = findViewById(R.id.textItem);

        for (int i = 0; i < y_pred_model_1.length; i++) {
            Log.i(" PREDICTION ", "Prediction results: " + String.valueOf(y_pred_model_1[i]));
        }
    }
    private int predict(int month, int gender) {
        float[] x_data = {month, gender};

        float[][] x_np = new float[1][2];
        x_np[0] = x_data;
        x_np[0][0] /= 12;
        x_np[0][1] /= 12;

        float[][] output = new float[1][7];
        localTfLiteModel.run(x_np, output);
        int[] y_pred_model_1 = argmax(output, 1);

        int finalPrediction = -1; // Set a default value in case y_pred_model_1 is empty

        for (int i = 0; i < y_pred_model_1.length; i++) {
            finalPrediction = y_pred_model_1[i];
            // You might want to do something else with each prediction here
        }

        return finalPrediction; // Return the final prediction after the loop
    }
    private void savePredictedCategory(int predictedCategoryNumber) {
        SharedPreferences sharedPreferences = getSharedPreferences("MyPrefs", MODE_PRIVATE);
        SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.putInt("predictedCategory", predictedCategoryNumber);
        editor.apply();
    }



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
}

