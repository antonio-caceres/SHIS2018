package edu.caceres.introhopfield;

import com.sun.org.apache.xalan.internal.xsltc.dom.MatchingIterator;

import java.io.Serializable;

public class Matrix implements Cloneable, Serializable {

    public static Matrix createColumnMatrix(final double input[]) {
        final double column[][] = new double[input.length][1];
        for (int r = 0; r < column.length; r++) {
            column[r][0] = input[r];
        }
        return new Matrix(column);
    }

    public static Matrix createRowMatrix(final double input[]) {
        final double row[][] = new double[1][input.length];
        // instead of this, Heaton had some arraycopy method that I didn't understand so I did this instead.
        for (int c = 0; c < row[0].length; c++) {
            row[0][c] = input[c];
        }
        return new Matrix(row);
    }

    public static Matrix createIdentityMatrix(final int size) {
        if(size < 1) {
            throw new IllegalArgumentException("The size of the identity matrix must be at least one. The specified size was " + size + ".");
        }
        final Matrix result = new Matrix(size, size);
        for (int i = 0; i < size; i++) {
            result.set(i, i, 1);
        }
        return result;
    }

    private double matrix[][];

    // creates a new matrix of 1s and -1s from a 2D Array of booleans
    public Matrix(final boolean sourceMatrix[][]) {
        this.matrix = new double[sourceMatrix.length][sourceMatrix[0].length];
        for (int r = 0; r < getRows(); r++) {
            for (int c = 0; c < getCols(); c++) {
                if (sourceMatrix[r][c]) {
                    set(r, c, 1);
                } else {
                    set(r, c, -1);
                }
            }
        }
    }

    // creates a new matrix from a 2D array of doubles
    public Matrix(final double sourceMatrix[][]) {
        this.matrix = new double[sourceMatrix.length][sourceMatrix[0].length];
        for (int r = 0; r < getRows(); r++) {
            for (int c = 0; c < getCols(); c++) {
                set(r, c, sourceMatrix[r][c]);
            }
        }
    }

    // creates a new empty matrix
    public Matrix(final int rows, final int cols) {
        this.matrix = new double[rows][cols];
        // I know it does this automatically. I just want it here for clarification.
        for (int r = 0; r < getRows(); r++) {
            for (int c = 0; c < getCols(); c++) {
                set(r, c, 0);
            }
        }
    }

    public void set(final int row, final int col, final double value) {
        if (Double.isInfinite(value) || Double.isNaN(value)) {
            throw new IllegalArgumentException("Trying to assign invalid number to matrix: "
                    + value);
        }
        this.matrix[row][col] = value;
    }

    public double get(final int row, final int col) {
        return matrix[row][col];
    }

    public void add(final int row, final int col, final double value) {
        if (Double.isInfinite(value) || Double.isNaN(value)) { // not exactly sure how these work
            throw new IllegalArgumentException("Trying to add invalid number to matrix: "
                    + value);
        }
        double newValue = get(row, col) + value;
        set(row, col, newValue);
    }

    public void clear() {
        for (int r = 0; r < getRows(); r++)
            for (int c = 0; c < getCols(); c++)
                set(r, c, 0);
    }

    public void randomize(final double min, final double max) {
        for (int r = 0; r < getRows(); r++) {
            for (int c = 0; c < getCols(); c++) {
                this.set(r, c, (Math.random() * (max - min)) + min);
            }
        }
    }

    // returns a row matrix of one row of the matrix
    public Matrix getRow(final int row) {
        final double newMatrix[][] = new double[1][getCols()];
        for (int col = 0; col < getCols(); col++) {
            newMatrix[0][col] = this.matrix[row][col];
        }
        return new Matrix(newMatrix);
    }

    public int getRows() {
        return this.matrix.length;
    }

    // returns a column matrix of one column of the matrix
    public Matrix getCol(final int col) {
        final double[][] newMatrix = new double[getRows()][1];

        for (int r = 0; r < getRows(); r++) {
            newMatrix[r][0] = this.matrix[r][col];
        }

        return new Matrix(newMatrix);
    }

    public int getCols() {
        return this.matrix[0].length;
    }

    public boolean equals(final Matrix matrix) {
        return equals(matrix, 10);
    }

    public boolean equals(final Matrix matrix, int precision) {

        if (precision < 0) {
            precision = 0;
        }

        final double test = Math.pow(10.0, precision);

        if (Double.isInfinite(test) || (test > Long.MAX_VALUE)) {
            throw new IllegalArgumentException("Precision of " + precision
                    + " decimal places is not supported.");
        }

        precision = (int) Math.pow(10, precision);

        for (int r = 0; r < getRows(); r++) {
            for (int c = 0; c < getCols(); c++) {
                if ((long) (get(r, c) * precision) != (long) (matrix.get(r, c) * precision)) {
                    return false;
                }
            }
        }

        return true;
    }

    public double[] toPackedArray() {
        double[] result = new double[getRows()*getCols()];
        int counter = 0;
        for (int r = 0; r < getRows(); r++) {
            for (int c = 0; c < getCols(); c++) {
                result[counter] = get(r, c);
                counter++;
            }
        }
        return result;
    }

    public int getArea() {
        return this.getRows() * this.getCols();
    }

    public double getSum() {
        double result = 0;
        for (int r = 0; r < getRows(); r++) {
            for (int c = 0; c < getCols(); c++) {
                result += get(r, c);
            }
        }

        return result;
    }

    public boolean isVectorMatrix() {
        return getRows() == 1 || getCols() == 1;
    }

    public boolean isZero() {
        for (int r = 0; r < getRows(); r++) {
            for (int c = 0; c < getCols(); c++) {
                if (this.matrix[r][c] != 0) {
                    return false;
                }
            }
        }
        return true;
    }

    @Override
    public String toString() {
        String matrixString = "";
        for (int r = 0; r < this.matrix.length; r++) {
            for (int c = 0; c < this.matrix[0].length; c++) {
                matrixString += this.matrix[r][c] + " ";
            }
            matrixString += "\n";
        }
        return matrixString;
    }

    @Override
    public Matrix clone() {
        return new Matrix(this.matrix);
    }
}
