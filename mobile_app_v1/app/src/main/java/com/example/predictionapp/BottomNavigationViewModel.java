package com.example.predictionapp;

import androidx.lifecycle.ViewModel;

public class BottomNavigationViewModel extends ViewModel {
    private int selectedTabIndex = 0; // Default tab index

    public int getSelectedTabIndex() {
        return selectedTabIndex;
    }

    public void setSelectedTabIndex(int index) {
        selectedTabIndex = index;
    }
}
