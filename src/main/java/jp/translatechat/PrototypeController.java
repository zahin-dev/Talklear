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
 // CHAT_METHODS
}
