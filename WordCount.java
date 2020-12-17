package wordcount;

import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class WordCount {
  // Map function
  public static class WordMapper extends Mapper<LongWritable, Text, Text, IntWritable>{
    private final static IntWritable one = new IntWritable(1);
    private Text word = new Text();
    public void map(LongWritable key, Text value, Context context) 
        throws IOException, InterruptedException {
      // Splitting the line on spaces
      String string = value.toString();

      /// Parse requirements.txt files && Parse setup.py files
      if ( string.length() > 0 && string.charAt(0) != '#') {	// not comment lines
		
	      int index1 = string.indexOf("=="); 	// get version
 	      int index2 = string.indexOf(">="); 	// get version
	      int index3 = string.indexOf("<="); 	// get version

	      if (index1 > 0 && string.length() > 0){
		string = string.substring(0, index1);
	      }
	      else if (index2 > 0 && string.length() > 0){
		string = string.substring(0, index2);
	      }
	      else if (index3 > 0 && string.length() > 0){
		string = string.substring(0, index3);
	      }
			
	      
	      String[] stringArr = string.toLowerCase().replaceAll("/"," ").replaceAll("[^a-zA-Z -_]","").split("\\s+");
	      for (String str : stringArr) {
		word.set(str);
		context.write(word, one);
	      }
      }  
    }
  }
	
  // Reduce function
  public static class CountReducer extends Reducer<Text, IntWritable, Text, IntWritable>{		   
    private IntWritable result = new IntWritable();
    public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
      int sum = 0;
      for (IntWritable val : values) {
        sum += val.get();
      }
      result.set(sum);
      context.write(key, result);
    }
  }
  
	
  public static void main(String[] args) throws Exception{
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "word count");
    job.setJarByClass(WordCount.class);
    job.setMapperClass(WordMapper.class);    
    job.setReducerClass(CountReducer.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);
    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}