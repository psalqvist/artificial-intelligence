  ;; Domain definition
(define (domain conference-domain)
  

(:predicates
	(ROOM ?x) ; true if x is a room
	(PERSON ?x) ; true if x is a person
	(TALK ?x) ; true if x is a talk
	(GROUP ?g) ; true if g is a lunch-group
	(IS-MORNING ?x) ; true if talk x is a morning talk
	(IS-AFTERNOON ?x) ; true if talk y is an afternoon talk
    (IS-CONNECTED ?x ?y) ; true if room x is connected to room y
    (IS-ATTENDEE ?x) ; true if person x is an attendee
    (IS-SPEAKER ?x) ; true if person x is a speaker
	(HAS-CATERING ?x) ; true if room x has catering 
    (IS-IN-GROUP ?x ?g) ; true if person x is in lunch-group g
    (IS-GROUP-AT ?g ?y); true if group g has lunch at room y
    (IS-TALK-AT ?x ?y) ; true if talk x is in room y
	(is-person-at ?x ?y) ; true if person x is in room y
	(attended-talk ?x ?y) ; true if person x has attended talk y
	(had-lunch ?x) ; true if person x has had lunch
    (gives-talk ?x ?y) ; true if speaker x gives talk y
)

; The person x moves from room y to room z if they are connected
; As a result, person x in no longer at y but they are at z
; Parameters:
; - x: the person
; - y: a room
; - z: another room
(:action move
    :parameters ( ?x ?y ?z )
    :precondition (and (PERSON ?x) (ROOM ?y) (ROOM ?z) (is-person-at ?x ?y) (IS-CONNECTED ?y ?z) )
    :effect (and (is-person-at ?x ?z) (not (is-person-at ?x ?y)))
)

; The attendee or the speaker x have lunch with their group g in room y that has catering.
; (If they haven't had lunch already)
; As a result they have lunch
; Parameters:
; - x: the person (attendee or speaker)
; - y: a room that has catering
; - g: the lunch-group where the person belongs to
(:action have-lunch 
	:parameters ( ?x ?y ?g )
	:precondition (and 
	    (PERSON ?x) 
	    (ROOM ?y) 
	    (GROUP ?g)
	    (HAS-CATERING ?y)
	    (IS-IN-GROUP ?x ?g)
	    (IS-GROUP-AT ?g ?y)
	    (not (had-lunch ?x))
	    (is-person-at ?x ?y)
	)
	:effect (had-lunch ?x)
)

; The attendee x attends the MORNING talk w given by speaker y inside room z
; (The attendee must NOT have had lunch before attending a morning talk)
; As a result the attendee x has attended the talk w
; Parameters:
; - x: an attendee
; - y: a speaker
; - z: a room
; - w: a talk
(:action attend-morning-talk
	:parameters ( ?x ?y ?z ?w )
	:precondition (and 
	    (PERSON ?x)
	    (IS-ATTENDEE ?x)
	    (not (had-lunch ?x))
	    (PERSON ?y)
	    (IS-SPEAKER ?y)
	    (ROOM ?z)
	    (TALK ?w)
	    (IS-MORNING ?w)
	    (gives-talk ?y ?w)
	    (is-person-at ?x ?z)
	    (is-person-at ?y ?z)
	    (IS-TALK-AT ?w ?z)
	)
	:effect (attended-talk ?x ?w)
)

; The attendee x attends the AFTERNOON talk w given by speaker y inside the room z
; (The attendee must have had lunch before being able to attend an afternoon talk)
; As a result the attendee x has attended the talk w
; Parameters:
; - x: an attendee
; - y: a speaker
; - z: a room
; - w: a talk
(:action attend-afternoon-talk
    :parameters (?x ?y ?z ?w)
    :precondition (and
        (PERSON ?x)
	    (IS-ATTENDEE ?x)
	    (had-lunch ?x)
	    (PERSON ?y)
	    (IS-SPEAKER ?y)
	    (ROOM ?z)
	    (TALK ?w)
	    (IS-AFTERNOON ?w)
	    (gives-talk ?y ?w)
	    (is-person-at ?x ?z)
	    (is-person-at ?y ?z)
	    (IS-TALK-AT ?w ?z)
    )
    :effect (attended-talk ?x ?w)
)

)
