import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class ToTips {
    public static void main(String[] args) throws ParseException, IOException {
        //String fullFileName = "C:/Java/workspace32/JudgerReviewToTips/src/test.json";
        //String outputFolder = "C:/Java/workspace32/JudgerReviewToTips/output";
        String workingDir = System.getProperty("user.dir");
    	String fullFileName = workingDir + '/' + args[0];
        String outputFolder = workingDir + '/' + args[1];
        System.out.println(fullFileName +"  "+ outputFolder);
        String outFileName = outputFolder + "/TipsOfReview";

        /*Read from .json file, form a real JSON file to StringBuilder sb*/
        File file = new File(fullFileName);
        Scanner scanner = null;
        StringBuilder sb = new StringBuilder();
        sb.append('[');
        try {
            scanner = new Scanner(file, "utf-8");
            while (scanner.hasNextLine()) {
                sb.append(scanner.nextLine());
                sb.append(',');
            }
        } catch (FileNotFoundException e) {
            // TODO Auto-generated catch block  
        } finally {
            if (scanner != null) {
            	sb.deleteCharAt(sb.length() - 1);
            	sb.append(']');
                scanner.close();
            }
        }
        
        /*Prepare output folder and file*/
        File file1 = new File(outputFolder); 
        if (file1.exists()) {  
            System.out.println("Existing outputFolder");  
        } else {  
            file1.mkdir(); // make folder
        }  
        File file2 = new File(outFileName);  
        if (file2.exists()) {  
            System.out.println("Existing file outFileName");  
        } else {  
            try {  
                file2.createNewFile(); 
            } catch (IOException e) {  
                // TODO Auto-generated catch block  
                e.printStackTrace();  
            }  
        }
        FileOutputStream fos = new FileOutputStream(file2); //Rewrite the whole file if exists
        OutputStreamWriter osw = new OutputStreamWriter(fos, "UTF-8");
        BufferedWriter bw = new BufferedWriter(osw);
       
        /*Deal with JSON file, print sentences to screen*/
        JSONArray jsonArr = (JSONArray) new JSONParser().parse(sb.toString());
        
        int size = jsonArr.size();
        System.out.println("Total reviews: " + size);

        /*For each review in JSON arr*/
        for (int i = 0; i < size; i++) {
            JSONObject jsonObject = (JSONObject) jsonArr.get(i);
            String text = (String) jsonObject.get("text");

            /*regular expression: end of sentence*/    
            String regEx="\\.|\\!|\\?";  // to be fixed?? Dr. & other char    
            Pattern p =Pattern.compile(regEx);     
            Matcher m = p.matcher(text);     
                
            /*split according to end char*/    
            String[] sentences = p.split(text);     
                
            /*append end char to each corresponding sentence*/    
            if(sentences.length > 0) {     
                int count = 0;     
                while(count < sentences.length) {   
                    if(m.find()) sentences[count] += m.group(); 
                    count++;     
                } 
            } 
                
            /*Print the sentence, receive tips from Judger*/  
            System.out.println("Review " + (i + 1) + "/" + size + ", total " + sentences.length + " sentences: ");  
            for(int index = 0; index < sentences.length; index++) {
                String sentence = sentences[index]; 
                System.out.println("[" + (index + 1) + "] " + sentence);     
            } 
            Scanner in;
            in = new Scanner(System.in);
            ArrayList tipNumList = new ArrayList();  //int
            System.out.println("Input # of tips:");     
            int numTips = in.nextInt();
            System.out.println("Input sentence # which are tips:");  
            for (int j = 0; j < numTips; j++) {
                int a = in.nextInt();
                tipNumList.add(a);         
            }
            System.out.println("---------------------------------\n");
            int[] tips = new int[sentences.length];
            //write to file2:
            bw.write("[" + jsonObject.get("review_id") + "] ");  
            for (int j = 0; j < tipNumList.size(); j++) {
                tips[Integer.parseInt(tipNumList.get(j).toString()) - 1] = 1;
            }
            for (Integer j : tips) bw.write(j.toString());  //System.out.print(j);
            bw.newLine(); 
        } // for each review

        // close data stream:
        bw.close();
        osw.close();
        fos.close();
        System.out.print("TipsOfReview successfully created!");
    }

}
