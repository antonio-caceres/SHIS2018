package edu.caceres.introhopfield;

public class MatrixMath {
    public static Matrix deleteRow(final Matrix matrix, final int deleted) {
        final double newMatrix[][] = new double[matrix.getRows() - 1][matrix.getCols()];
        int targetRow = 0;
        for (int r = 0; r < matrix.getRows(); r++) {
            if (r != deleted) {
                for (int c = 0; c < matrix.getCols(); c++) {
                    newMatrix[targetRow][c] = matrix.get(r, c);
                }
                targetRow++;
            }
        }
        return new Matrix(newMatrix);
    }

    public static Matrix deleteCol(final Matrix matrix, final int deleted) {
        final double newMatrix[][] = new double[matrix.getRows()][matrix.getCols() - 1];
        for (int r = 0; r < matrix.getRows(); r++) {
            int targetCol = 0;
            for (int c = 0; c < matrix.getCols(); c++) {
                if (c != deleted) {
                    newMatrix[r][targetCol] = matrix.get(r, c);
                    targetCol++;
                }

            }

        }
        return new Matrix(newMatrix);
    }

    public static Matrix add(final Matrix a, final Matrix b) {
        return MatrixMath.add(a, b, false);
    }

    public static Matrix add(final Matrix a, final Matrix b, boolean subtract) {
        if (a.getRows() != b.getRows() || a.getCols() != b.getCols())
            throw new IllegalArgumentException("Two matrices must have the same number of rows and columns to add them. " +
                    "a has " + a.getRows() + " and " + a.getCols() + ". " +
                    "b has " + b.getRows() + " and " + b.getCols() + ".");
        Matrix resultMatrix = new Matrix(a.getRows(), a.getCols());

        for (int r = 0; r < a.getRows(); r++) {
            for (int c = 0; c < a.getCols(); c++) {
                double value;
                if(subtract)
                    value = a.get(r, c) - b.get(r, c);
                else
                    value = a.get(r, c) + b.get(r, c);
                resultMatrix.set(r, c, value);
            }
        }

        return resultMatrix;
    }

    public static void copy(final Matrix source, final Matrix target) {
        for (int row = 0; row < source.getRows(); row++) {
            for (int col = 0; col < source.getCols(); col++) {
                target.set(row, col, source.get(row, col));
            }
        }
    }

    public static Matrix scalarMultiply(final Matrix matrix, final double scalar) {
        final double result[][] = new double[matrix.getRows()][matrix.getCols()];
        for (int r = 0; r < matrix.getRows(); r++) {
            for (int c = 0; c < matrix.getCols(); c++) {
                result[r][c] = matrix.get(r, c) * scalar;
            }
        }
        return new Matrix(result);
    }

    public static Matrix scalarDivide(final Matrix matrix, final double scalar) {
        final double result[][] = new double[matrix.getRows()][matrix.getCols()];
        for (int r = 0; r < matrix.getRows(); r++) {
            for (int c = 0; c < matrix.getCols(); c++) {
                result[r][c] = matrix.get(r, c) / scalar;
            }
        }
        return new Matrix(result);
    }

    public static double dotProduct(final Matrix matrixA, final Matrix matrixB) {
        if (!matrixA.isVectorMatrix() || !matrixB.isVectorMatrix()) {
            throw new IllegalArgumentException("To take the dot product of two matrices, they must both be vector matrices.");
        }

        final double[] arrayA = matrixA.toPackedArray();
        final double[] arrayB = matrixB.toPackedArray();

        if (arrayA.length != arrayB.length) {
            throw new IllegalArgumentException("To take the dot product, both matrices must be of the same length." +
                    "Array A is of length " + arrayA.length + ". Array B is of length " + arrayB.length + ".");
        }

        double result = 0;

        for (int i = 0; i < arrayA.length; i++) {
            result += arrayA[i] * arrayB[i];
        }

        return result;
    }

    public static Matrix matrixMultiply(final Matrix a, final Matrix b) {
        if (a.getCols() != b.getRows()) {
            throw new IllegalArgumentException(
                    "To use ordinary matrix multiplication the number of columns on the first matrix must match the number of rows on the second.");
        }

        final double result[][] = new double[a.getRows()][b.getCols()];

        for (int resultRow = 0; resultRow < a.getRows(); resultRow++) {
            for (int resultCol = 0; resultCol < b.getCols(); resultCol++) {
                double value = 0;

                for (int i = 0; i < a.getCols(); i++) {
                    value += a.get(resultRow, i) * b.get(i, resultCol);
                }
                result[resultRow][resultCol] = value;
            }
        }

        return new Matrix(result);
    }

    public static Matrix transpose(final Matrix input) {
        final double inverseMatrix[][] = new double[input.getCols()][input
                .getRows()];
        for (int r = 0; r < input.getRows(); r++) {
            for (int c = 0; c < input.getCols(); c++) {
                inverseMatrix[c][r] = input.get(r, c);
            }
        }
        return new Matrix(inverseMatrix);
    }

    public static double vectorLength(final Matrix input) {
        if (!input.isVectorMatrix()) {
            throw new IllegalArgumentException("Can only take the vector length of a vector.");
        }
        final double[] v = input.toPackedArray();
        double rtn = 0.0;
        for (int i = 0; i < v.length; i++) {
            rtn += Math.pow(v[i], 2);
        }
        return Math.sqrt(rtn);
    }
}
