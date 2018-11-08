package edu.caceres.introhopfield;

import javax.swing.*;
import java.awt.*;

/*
work in progress; delayed for now because GUI is not central to my project.
 */
public class HopfieldApp {

    JFrame frame;
    int numNeurons;

    public HopfieldApp() {
        frame = new JFrame("Hopfield Neural Network Application");
        // TODO prompt for num Neurons
        if(numNeurons > 10) {
            numNeurons = 10;
            // TODO dialog warning
        }
        numNeurons = 6;
        frame.setSize(numNeurons*60 + 90,300); // 50 width per neuron + 100, + 10 for neurons - 1.
        frame.setLayout(null);
        frame.setVisible(true);
    }

    public void initGUI() {
        initJLabels();
        initTextFields();
        initButtons();
        frame.repaint();
    }

    public void initJLabels() { // TODO initialize JLabel
        JLabel arrayLabel = new JLabel("Array");
        frame.add(arrayLabel);
    }

    public void initTextFields() { // TODO initialize text fields

    }

    public void initButtons() { // TODO initialize train and present buttons

    }

    public static void main(String[] args) {
        HopfieldApp app = new HopfieldApp();
        app.initGUI();
    }
}
