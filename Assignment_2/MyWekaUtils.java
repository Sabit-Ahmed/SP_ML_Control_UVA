

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.PrintWriter;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.Stream;

import weka.classifiers.Classifier;
import weka.classifiers.Evaluation;
import weka.classifiers.functions.SMO;
import weka.classifiers.trees.J48;
import weka.classifiers.trees.RandomForest;
import weka.core.Instances;
import weka.core.pmml.jaxbbindings.False;


/**
 *
 * @author mm5gg
 * modified by author bcw3zj
 */
public class MyWekaUtils {

    public static double classify(String arffData, int option) throws Exception {
		StringReader strReader = new StringReader(arffData);
		Instances instances = new Instances(strReader);
		strReader.close();
		instances.setClassIndex(instances.numAttributes() - 1);

		Classifier classifier;
		if(option==1)
			classifier = new J48(); // Decision Tree classifier
		else if(option==2)
			classifier = new RandomForest();
		else if(option == 3)
			classifier = new SMO();  //This is a SVM classifier
		else
			return -1;

		classifier.buildClassifier(instances); // build classifier

		Evaluation eval = new Evaluation(instances);
		eval.crossValidateModel(classifier, instances, 10, new Random(1), new Object[] { });

		return eval.pctCorrect();
	}


    public static String[][] readCSV(String filePath) throws Exception {
        StringBuilder sb = new StringBuilder();
        BufferedReader br = new BufferedReader(new FileReader(filePath));
        ArrayList<String> lines = new ArrayList();
        String line;

        while ((line = br.readLine()) != null) {
            lines.add(line);;
        }


        if (lines.size() == 0) {
            System.out.println("No data found");
            return null;
        }

        int lineCount = lines.size();

        String[][] csvData = new String[lineCount][];
        String[] vals;
        int i, j;
        for (i = 0; i < lineCount; i++) {
                csvData[i] = lines.get(i).split(",");
        }

        return csvData;

    }

    public static String csvToArff(String[][] csvData, int[] featureIndices) throws Exception {
        int total_rows = csvData.length;
        int total_cols = csvData[0].length;
        int fCount = featureIndices.length;
        String[] attributeList = new String[fCount + 1];
        int i, j;
        for (i = 0; i < fCount; i++) {
            attributeList[i] = csvData[0][featureIndices[i]];
        }
        attributeList[i] = csvData[0][total_cols - 1];

        String[] classList = new String[1];
        classList[0] = csvData[1][total_cols - 1];

        for (i = 1; i < total_rows; i++) {
            classList = addClass(classList, csvData[i][total_cols - 1]);
        }

        StringBuilder sb = getArffHeader(attributeList, classList);

        for (i = 1; i < total_rows; i++) {
            for (j = 0; j < fCount; j++) {
                sb.append(csvData[i][featureIndices[j]]);
                sb.append(",");
            }
            sb.append(csvData[i][total_cols - 1]);
            sb.append("\n");
        }

        return sb.toString();
    }

    private static StringBuilder getArffHeader(String[] attributeList, String[] classList) {
        StringBuilder s = new StringBuilder();
        s.append("@RELATION wada\n\n");

        int i;
        for (i = 0; i < attributeList.length - 1; i++) {
            s.append("@ATTRIBUTE ");
            s.append(attributeList[i]);
            s.append(" numeric\n");
        }

        s.append("@ATTRIBUTE ");
        s.append(attributeList[i]);
        s.append(" {");
        s.append(classList[0]);

        for (i = 1; i < classList.length; i++) {
            s.append(",");
            s.append(classList[i]);
        }
        s.append("}\n\n");
        s.append("@DATA\n");
        return s;
    }

    private static String[] addClass(String[] classList, String className) {
        int len = classList.length;
        int i;
        for (i = 0; i < len; i++) {
            if (className.equals(classList[i])) {
                return classList;
            }
        }

        String[] newList = new String[len + 1];
        for (i = 0; i < len; i++) {
            newList[i] = classList[i];
        }
        newList[i] = className;

        return newList;
    }

    public static int getIndexOfLargest( double[] array )
    {
        if ( array == null || array.length == 0 ) return -1; // null or empty
        int largest = 0;

        for ( int i = 1; i < array.length; i++ ) {
            if ( array[i] > array[largest] ) largest = i;
        }

        return largest; // position of the first largest found
    }

    public static int[] getSliceOfArray(int[] arr, int startIndex, int endIndex) {

        // Get the slice of the Array
        int[] slice = IntStream

        // Convert the specified elements
        // of array into IntStream
        .range(startIndex, endIndex)

        // Lambda expression to get
        // the elements of IntStream
        .map(i -> arr[i])

        // Convert the mapped elements
        // into the slice array
        .toArray();

        // return the slice
        return slice;
    }

    public static String getClassifierName(int option) {
        String classifier = "Unknown";
        if(option==1)
			classifier = "Decision Tree Classifier"; // Decision Tree classifier
		else if(option==2)
			classifier = "Random Forest Classifier";
		else if(option == 3)
			classifier = "SVM Classifier";  //This is a SVM classifier

        return classifier;
    }

    public static void selectFeatures(int classifyOption) {
        try {
            String[][] csvData = readCSV("Assignment_2/preprocessdata/4sec.csv");
            int nFeatures = 12;
            List<Integer> selectedFeatures = new ArrayList<>();
            List<Double> selectedFeaturesResults = new ArrayList<>();
            while (selectedFeatures.size() < nFeatures) {
                String arffData = "";
                double result = 0;
                double[] resultArray = new double [nFeatures];
                int i;
                for (i = 0; i < nFeatures; i++) {
                    if (!selectedFeatures.contains(i)) {
                        selectedFeatures.add(i);
                        int[] featureIndices = selectedFeatures.stream().mapToInt(j -> j).toArray();
                        arffData = csvToArff(csvData, featureIndices);
                        result = classify(arffData, classifyOption);
                        String printString = "Feature set " + Arrays.toString(featureIndices)
                        + "---->" + " accuracy ::" + result;
                        System.out.println(printString);
                        resultArray[i] = result;
                        selectedFeatures.removeLast();
                    }
                }
                int bestFeatureIndex = getIndexOfLargest(resultArray);
                selectedFeatures.add(bestFeatureIndex);
                double bestFeatureResult = resultArray[bestFeatureIndex];
                selectedFeaturesResults.add(bestFeatureResult);
                System.out.println("Selected features ::" + selectedFeatures);
                // System.out.println(selectedFeaturesResults);

            }

            double[] selectedFeaturesResultsArray = selectedFeaturesResults.stream().mapToDouble(k -> k).toArray();
            int bestFeatureLastIndex = getIndexOfLargest(selectedFeaturesResultsArray);

            int[] bestFeatureIndicesFinal = getSliceOfArray(selectedFeatures.stream().mapToInt(k -> k).toArray(), 0, bestFeatureLastIndex + 1);
            double bestFeatureResultFinal = selectedFeaturesResultsArray[bestFeatureLastIndex];

            System.out.println(getClassifierName(classifyOption) + "--->" + "Best feature set:: " + Arrays.toString(bestFeatureIndicesFinal));
            System.out.println("Best feature set accuracy:: " + bestFeatureResultFinal);
        }
        catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
	// some code here in the main() method
        MyWekaUtils wekaObject = new MyWekaUtils();
        try {
            wekaObject.selectFeatures(1);
            wekaObject.selectFeatures(2);
            wekaObject.selectFeatures(3);
        } catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }
}

