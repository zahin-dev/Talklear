package jp.translatechat;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.http.HttpStatus;
/** Simulated local-only prototype. Volatile memory, no identity verification. */
@RestController @RequestMapping("/api")
class PrototypeController {
 record Join(String displayName, String language) {}
 record Entry(String roomCode, String displayName) {}
 final Map<String,List<Entry>> rooms = new ConcurrentHashMap<>();
 void validate(Join j) { if(j==null || j.displayName()==null || j.displayName().isBlank()) throw new ResponseStatusException(HttpStatus.BAD_REQUEST); }
 @PostMapping("/rooms") Entry create(@RequestBody Join j) { validate(j); String code=UUID.randomUUID().toString().replace("-", "").substring(0,12).toUpperCase(); rooms.put(code,Collections.synchronizedList(new ArrayList<>()));return join(code,j); }
 @PostMapping("/rooms/{code}/join") Entry join(@PathVariable String code,@RequestBody Join j) { validate(j);var room=rooms.get(code);if(room==null)throw new ResponseStatusException(HttpStatus.NOT_FOUND);var e=new Entry(code,j.displayName());room.add(e);return e; }
 record Send(String text) {}
 record Message(long id, String text) {}
 final Map<String,List<Message>> messages = new ConcurrentHashMap<>();
 @PostMapping("/rooms/{code}/messages") synchronized Message send(@PathVariable String code,@RequestBody Send s) {if(!rooms.containsKey(code))throw new ResponseStatusException(HttpStatus.NOT_FOUND);if(s==null||s.text()==null||s.text().isBlank())throw new ResponseStatusException(HttpStatus.BAD_REQUEST);var list=messages.computeIfAbsent(code,k->new ArrayList<>());var m=new Message(list.size()+1,s.text());list.add(m);return m;}
 @GetMapping("/rooms/{code}/state") synchronized List<Message> state(@PathVariable String code) {if(!rooms.containsKey(code))throw new ResponseStatusException(HttpStatus.NOT_FOUND);return List.copyOf(messages.getOrDefault(code,List.of()));}

}
