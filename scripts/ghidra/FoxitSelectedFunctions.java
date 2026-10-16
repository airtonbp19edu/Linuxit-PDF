import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;
import ghidra.util.task.ConsoleTaskMonitor;
import com.google.gson.GsonBuilder;
import java.nio.file.*;
import java.util.*;

public class FoxitSelectedFunctions extends GhidraScript {
  @Override public void run() throws Exception {
    String[] args=getScriptArgs();
    if(args.length!=2)throw new IllegalArgumentException("seeds.tsv output-directory");
    Path out=Path.of(args[1]);Files.createDirectories(out);
    DecompInterface decompiler=new DecompInterface();
    if(!decompiler.openProgram(currentProgram))throw new IllegalStateException(decompiler.getLastMessage());
    try {
      for(String row:Files.readAllLines(Path.of(args[0]))) {
        if(row.isBlank())continue;
        String[] fields=row.split("\t");Address address=toAddr(Long.parseUnsignedLong(fields[0].substring(2),16));
        Function function=getFunctionAt(address);
        if(function==null) {disassemble(address);function=createFunction(address,fields.length>2?fields[2]:null);}
        Map<String,Object> data=new LinkedHashMap<>();
        data.put("entry_va",fields[0]);data.put("origin","direct Ghidra backend; REA seed script; headless -noanalysis");
        if(function==null)data.put("error","Function entry could not be created");
        else {
          data.put("analyst_name",function.getName());data.put("signature_hint",function.getSignature().toString());
          DecompileResults result=decompiler.decompileFunction(function,45,monitor);
          data.put("decompile_completed",result.decompileCompleted());data.put("decompiler_message",result.getErrorMessage());
          if(result.getDecompiledFunction()!=null)data.put("pseudocode",result.getDecompiledFunction().getC());
          List<String> assembly=new ArrayList<>();
          for(Instruction instruction:currentProgram.getListing().getInstructions(function.getBody(),true))
            assembly.add(instruction.getAddress()+": "+instruction.toString());
          data.put("assembly",assembly);data.put("body_bytes",function.getBody().getNumAddresses());
          data.put("body_ranges",function.getBody().toString());
        }
        Files.writeString(out.resolve(fields[0]+".json"),new GsonBuilder().setPrettyPrinting().create().toJson(data));
        println("FOXIT ENTRY "+fields[0]+" "+data.get("decompile_completed"));
      }
    } finally {decompiler.dispose();}
  }
}
