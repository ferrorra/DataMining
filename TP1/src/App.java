import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Map;
import java.util.OptionalDouble;
import java.util.HashMap;
import java.util.Collections;



public class App {

    private static Integer SIZE = 0;

    private static ArrayList<Double> sepal_length_in_cm = new ArrayList<Double>();
    private static ArrayList<Double> sepal_width_in_cm = new ArrayList<Double>();
    private static ArrayList<Double> petal_length_in_cm = new ArrayList<Double>();
    private static ArrayList<Double> petal_width_in_cm = new ArrayList<Double>();
    private static ArrayList<String> type = new ArrayList<String>();

    //1-methode pour charger le dataset
    public static BufferedReader ChargerData() throws FileNotFoundException{
    //charger dataset
        return new BufferedReader(new FileReader("resources\\Dataset-Exos.txt"));
    }

    public static void Describe(){
        BufferedReader dataset=null;
        String line =null;
        String[] infos = new String[]{null,null,null,null,null};

        //afficher infos bases dataset
        try{


        dataset = ChargerData();
        while ((line=dataset.readLine())!=null){
            //System.out.println(line);
            infos = line.split(",");
            if(infos[0] != null && !infos[0].isEmpty()) sepal_length_in_cm.add(Double.parseDouble(infos[0]));
            if(infos[1] != null && !infos[1].isEmpty()) sepal_width_in_cm.add(Double.parseDouble(infos[1]));
            if(infos[2] != null && !infos[2].isEmpty()) petal_length_in_cm.add(Double.parseDouble(infos[2]));
            if(infos[3] != null && !infos[3].isEmpty()) petal_width_in_cm.add(Double.parseDouble(infos[3]));
            if(infos.length >4)  type.add(infos[4]);
            dataset.readLine();
            }


            SIZE = Collections.max(new ArrayList<Integer>(){
                { add(sepal_length_in_cm.size()); 
                add(sepal_width_in_cm.size()); 
                add(petal_length_in_cm.size()); 
                add(petal_width_in_cm.size()); 
                add(type.size());
                }
            });



            //show dataframe
            head(5);

            System.out.println("GENERAL INFORMATION*****************************************************");
            System.out.println("A.) sepal_length_in_cm ...................................." );
            statsNonCategorical(sepal_length_in_cm);

            System.out.println("B.) sepal_width_in_cm ...................................." );
            statsNonCategorical(sepal_width_in_cm);


            System.out.println("C.) petal_length_in_cm ...................................." );
            statsNonCategorical(petal_length_in_cm);


            System.out.println("D.) petal_width_in_cm ...................................." );
            statsNonCategorical(petal_width_in_cm);


            System.out.println("E.) type ...................................." );
            statsCategorical(type);


            System.out.println("MISSING VALUES REPPORT*****************************************************");

            ValeurManquantes(sepal_length_in_cm,"sepal_length_in_cm");
            ValeurManquantes(sepal_width_in_cm,"sepal_width_in_cm");
            ValeurManquantes(petal_length_in_cm,"petal_length_in_cm");
            ValeurManquantes(petal_width_in_cm,"petal_width_in_cm");
            ValeurManquantesCatgorical(type,"type");

        }catch(Exception e){
            System.out.println("There is a problem with your file" );
            e.printStackTrace();
        }
    }



    public static void statsNonCategorical(ArrayList<Double> liste){


        /* count == number of total values 
        mean == la moyenne of values
         */

        int count;
        Double std, min = Collections.min(liste), max = Collections.max(liste), median;
        OptionalDouble mean;

        count = liste.size();


        mean = liste.stream().mapToDouble(a -> a).average();

        /* Calculating the standard devitation ;
         * Step 1: Find the mean.
            Step 2: For each data point, find the square of its distance to the mean.
            Step 3: Sum the values from Step 2.
            Step 4: Divide by the number of data points.
         */
        double temp = 0;

        for (int i = 0; i < liste.size(); i++)
        {
            Double val = liste.get(i);
    
            // Step 2:
            Double squrDiffToMean = Math.pow(val - mean.orElse(temp), 2);
    
            // Step 3:
            temp += squrDiffToMean;
        }
    
        // Step 4:
        double meanOfDiffs = (double) temp / (double) (liste.size());

        std = Math.sqrt(meanOfDiffs);

        Collections.sort(liste);
        int middle = liste.size() / 2;
        middle = middle > 0 && middle % 2 == 0 ? middle - 1 : middle;
        median =  liste.get(middle);

        System.out.println("+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+SHOWING STATS FPR A NON CATEGORICAL Attribute+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+");
        System.out.println( "COUNT : " +count);
        System.out.println( "MEAN : " +mean);
        System.out.println( "STANDARD DEVIATION : " +std);
        System.out.println( "MEDIAN : " +median);

        System.out.println( "MIN VALUE : " +min);
        System.out.println( "MAX VALUE : " +max);

        System.out.println("PENCENTILES VALUES :");

        System.out.println( "25% Q1: " +percentile(liste, 25));
        System.out.println( "50% Q2: " +percentile(liste, 50));
        System.out.println( "75% Q3: " +percentile(liste, 75));
        System.out.println( "100% Q4: " +percentile(liste, 100));




    }

    public static Double percentile(ArrayList<Double> latencies, double percentile) {
        int index = (int) Math.ceil(percentile / 100.0 * latencies.size());
        return latencies.get(index-1);
    }


    public static void statsCategorical(ArrayList<String> liste){

        /* count == number of total values 
         * unique == number of categories 
         * values, occ == list of all categories and their frequency 
         * top (mode) == category with highest frequency 
         * freq == highest frequency
         */
        int count, unique;
        String median;


        Map<String, Integer> hm = new HashMap<String, Integer>(); //type/frequency



        String top = "";
        int freq;



        count = liste.size();

        HashSet noDupSet = new HashSet(liste);
        unique = noDupSet.size();

        //counting frequencies

 
        for (String i : liste) {
            Integer j = hm.get(i);
            hm.put(i, (j == null) ? 1 : j + 1); //if elt doesnt exist we add it, else we increment key value
        }
        freq = Collections.max(hm.values());
 
        // displaying the occurrence of elements 
        for (Map.Entry<String, Integer> val : hm.entrySet()) {

            if (val.getValue() == freq) {

                top = val.getKey();     // this is the key which has the max value
            }




        }

        Collections.sort(liste);
        int middle = liste.size() / 2;
        middle = middle > 0 && middle % 2 == 0 ? middle - 1 : middle;
        median =  liste.get(middle);


        System.out.println("+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+SHOWING STATS FOR A CATEGORICAL Attribute+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+");
            System.out.println( "COUNT : " +count);
            System.out.println( "UNIQUE VALUES NUMBER : " +unique);
            System.out.println( "TOP CATEGORY : " +top);
            System.out.println( "TOP FREQUENCY : " +freq);
            System.out.println( "MEDIAN : " +median);


            System.out.println("ALL CATGORIES AND THEIR FREQUENCIES :");

            hm.entrySet().forEach(entry -> {
            System.out.println(entry.getKey() + " " + entry.getValue());
            });


    }


    public static void head(int taille){
            System.out.println(String.format("%10s %20s %10s %20s %10s %20s %10s %20s %10s %20s %10s ", "|","sepal_length_in_cm","|",  "sepal_width_in_cm" ,"|", "petal_length_in_cm", "|" ,"petal_length_in_cm", "|", "type", "|")); 
            System.out.println(String.format("%s","---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"));

            for(int i=0; i<taille;i++){
                System.out.println(String.format("%10s %20f %10s %20f %10s %20f %10s %20f %10s %20s %10s","|", sepal_length_in_cm.get(i), "|", sepal_width_in_cm.get(i), "|", petal_length_in_cm.get(i), "|", petal_width_in_cm.get(i), "|", type.get(i) , "|"));
                System.out.println(String.format("%s","---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"));
            }
    }


    public static void ValeurManquantes(ArrayList<Double> elts, String name) throws NoSuchFieldException{
        //nombre et pourcentage de valeur manquantes
        if(elts.size() < SIZE) {
            System.out.println( "There are values missing in :" + name);
            Integer missing =   SIZE - elts.size();
            System.out.println( "Number of missing values :" +  missing);
            double pourcentage = 100*missing/(double)SIZE;
            System.out.println( "Pourcentage of missing values : " +pourcentage+"%" );
        }
}

public static void ValeurManquantesCatgorical(ArrayList<String> elts, String name) throws NoSuchFieldException{
    //nombre et pourcentage de valeur manquantes
    if(elts.size() < SIZE) {
        System.out.println( "There are values missing in :" + name);
        int missing = SIZE - elts.size();
        System.out.println( "Number of missing values :" +  missing);
        double pourcentage = 100*missing/(double)SIZE;
        System.out.println( "Pourcentage of missing values : " +pourcentage+"%" );
    }
}

    public static void main(String[] args) throws Exception {
        try{
            Describe();

        }catch (Exception e){
            System.out.println("There is a problem with your file");

        }
    }
}
