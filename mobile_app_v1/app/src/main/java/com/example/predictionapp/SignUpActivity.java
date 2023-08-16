package com.example.predictionapp;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.RadioGroup;
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




public class SignUpActivity extends AppCompatActivity {
    private EditText etName, etAge, etEmail, etCity,etPassword,etReenterPassword;
    //EditText etPassword = findViewById(R.id.etPassword);

    private RadioGroup etGender;
    Interpreter localTfliteModel;
    Interpreter receivedTfliteModel;
    private Button signUpButton; // Declare the button

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.signup_layout);

        // Initialize the button by finding it in the layout
        signUpButton = findViewById(R.id.btnSignUp);



        // Initialize EditText fields
        etName = findViewById(R.id.EditName);
        etEmail = findViewById(R.id.etEmail);
        etAge = findViewById(R.id.etAge);
        etGender = findViewById(R.id.radioGroupGender);
        etCity = findViewById(R.id.etCity);
        etPassword = findViewById(R.id.etPassword);
        etReenterPassword = findViewById(R.id.etReenterPassword);


        // Set a click listener for the button
        signUpButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // This code will be executed when the button is clicked
                // Call the method to save user data to JSON and navigate to login
                saveFormJson();
            }
        });
    }

    // ... (Your code for form handling and other functionalities)
        private void saveFormJson() {
            String name = etName.getText().toString();
            int selectedGenderId = etGender.getCheckedRadioButtonId();
            String email = etEmail.getText().toString();
            String age = etAge.getText().toString();
            String city = etCity.getText().toString();
            String password = etPassword.getText().toString();
            String reenteredPassword = etReenterPassword.getText().toString();

            if (name.isEmpty()) {
                etName.setError("Name is required");
                etName.requestFocus();
                return;
            }

            if (selectedGenderId == -1) {
                // No gender is selected
                TextView errorText = (TextView) etGender.getChildAt(0);
                errorText.setError("Gender is required");
                etGender.requestFocus();
                return;
            }

            if (email.isEmpty()) {
                etEmail.setError("Email is required");
                etEmail.requestFocus();
                return;
            }
            if (age.isEmpty()) {
                etAge.setError("Age is required");
                etAge.requestFocus();
                return;
            }

            if (city.isEmpty()) {
                etCity.setError("City is required");
                etCity.requestFocus();
                return;
            }
            if (password.isEmpty()) {
                etCity.setError("Password is required");
                etCity.requestFocus();
                return;
            }
            if (reenteredPassword.isEmpty()) {
                etCity.setError("Please verify your password");
                etCity.requestFocus();
                return;
            }
            String selectedGender = "";
            if (selectedGenderId == R.id.radioButtonMale) {
                selectedGender = "Male";
            } else if (selectedGenderId == R.id.radioButtonFemale) {
                selectedGender = "Female";
            }
            if(password != reenteredPassword){
                etReenterPassword.setError("password is not match..");
            }
            // Create a JSON object to hold the user data
            JSONObject userDataJson = new JSONObject();
            try {
                userDataJson.put("name", name);
                userDataJson.put("gender", selectedGender);
                userDataJson.put("email",email);
                userDataJson.put("age", age);
                userDataJson.put("city", city);
                userDataJson.put("password",password);
            } catch (JSONException e) {
                e.printStackTrace();
            }

            // Create the file name
            String userDataJsonFile = "user_data.json";

            String existingFormData = readFormData();

            if (existingFormData != null && existingFormData.contains(userDataJson.toString())) {
                // Check whether a user exists or not
                Toast.makeText(getApplicationContext(), "This user has been already added", Toast.LENGTH_SHORT).show();
            } else {
                try {
                    FileOutputStream fileOutputStream = openFileOutput(userDataJsonFile, Context.MODE_APPEND);
                    // Convert the JSON object to a JSON string
                    String userDataJsonString = userDataJson.toString() + "\n";
                    fileOutputStream.write(userDataJsonString.getBytes());
                    fileOutputStream.close();
                    Calendar calendar = Calendar.getInstance();
                    /*loadModel("model");
                    int currentMonth = calendar.get(Calendar.MONTH) + 1;
                    int genderInt=0;
                    if(selectedGender == "Female"){genderInt = 1;}
                    if(selectedGender == "Male"){genderInt = 0;}
                    predict(currentMonth, genderInt);*/
                    // Clear the text boxes
                    etName.setText("");
                    etGender.clearCheck();
                    etEmail.setText("");
                    etAge.setText("");
                    etCity.setText("");
                    etPassword.setText("");
                    etReenterPassword.setText("");

                    // Show success message or navigate to login screen
                    Toast.makeText(this, "User registered successfully", Toast.LENGTH_SHORT).show();
                    navigateToLogin(); // Call your method to navigate to the login screen

                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
        private void navigateToLogin() {
            Intent intent = new Intent(this, LoginActivity.class);
            startActivity(intent);
            //finish(); // Optional: Close the current activity if you don't want the user to come back to it
        }
        private String readFormData() {
            try {
                FileInputStream fis = openFileInput("user_data.json");
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
    }private MappedByteBuffer loadFile(String fileName) throws IOException {
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

        //TextView txtPredictItem = findViewById(R.id.textItem);

        for (int i = 0; i < y_pred_model_1.length; i++) {
            Log.i(" Prediction App ", "Prediction results: " + String.valueOf(y_pred_model_1[i]));
        }
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



