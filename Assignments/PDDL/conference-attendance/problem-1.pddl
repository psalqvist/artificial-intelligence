;; Problem definition
(define (problem problem-1)

  ;; Specifying the domain for the problem
  (:domain conference-domain)

  ;; Objects definition
  (:objects
    ; Rooms
    R1
    R2
    R3
    R4
   ; Persons (Attendees and speakers)
    A1
    S1
    S2
    ; Talks
    T1
    T2
    T3
    ; groups (for lunch)
    G1
  )

  ;; Intial state of problem 1
  (:init
    ;; Declaration of the objects
    ; Rooms
    (ROOM R1)
    (ROOM R2)
    (ROOM R3)
    (ROOM R4)
    ; People (Attendees and speakers)
    (PERSON A1)
    (PERSON S1)
    (PERSON S2)
    ; Talks
    (Talk T1)
    (Talk T2)
    (Talk T3)
    ; Lunch groups
    (GROUP G1)
    
    ;; Declaration of the predicates of the objects
    ; We set people locations
    (is-person-at A1 R4)
    (is-person-at S1 R2)
    (is-person-at S2 R3)
   
    ; We set the rooms where talks take place
    (IS-TALK-AT T1 R1)
    (IS-TALK-AT T2 R2)
    (IS-TALK-AT T3 R3)
    (IS-TALK-AT T1 R4)
    (IS-TALK-AT T3 R4)
    
    ; We set whether the talk is a morning or afternoon talk
    (IS-MORNING T1)
    (IS-MORNING T2)
    (IS-AFTERNOON T2)
    (IS-AFTERNOON T3)

    ; We set whether the room has catering
    (HAS-CATERING R3)
    
    ; We check in which lunch-group the person is
    (IS-IN-GROUP A1 G1)
    (IS-IN-GROUP S1 G1)
    (IS-IN-GROUP S2 G1)
    
    ; We check in which room the lunch-group is placed
    (IS-GROUP-AT G1 R3) 

    ; We set whether the person is a speaker or an attendee
    (IS-SPEAKER S1)
    (IS-SPEAKER S2)
    (IS-ATTENDEE A1)

    ; We set which speaker gives which talk
    (gives-talk S1 T1)
    (gives-talk S1 T2)
    (gives-talk S2 T3)
    
    ; We set the connections between the rooms
    (IS-CONNECTED R1 R2) (IS-CONNECTED R2 R1) 
    (IS-CONNECTED R2 R3) (IS-CONNECTED R3 R2) 
    (IS-CONNECTED R3 R4) (IS-CONNECTED R4 R3) 
  )

  ;; Goal specification
  (:goal
    (and
      (attended-talk A1 T1)
      (attended-talk A1 T2)
      (attended-talk A1 T3)

      (had-lunch A1)
      (had-lunch S1)
      (had-lunch S2)
    )
  )

)
