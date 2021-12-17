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
    R5
    R6
   ; Persons (Attendees and speakers)
    A1
    A2
    A3
    S1
    S2
    S3
    ; Talks
    T1
    T2
    T3
    T4
    T5
    T6
    ; groups (for lunch)
    G1
    G2
  )

  ;; Intial state of problem 1
  (:init
    ;; Declaration of the objects
    ; Rooms
    (ROOM R1)
    (ROOM R2)
    (ROOM R3)
    (ROOM R4)
    (ROOM R5)
    (ROOM R6)
    ; People (Attendees and speakers)
    (PERSON A1)
    (PERSON A2)
    (PERSON A3)
    (PERSON S1)
    (PERSON S2)
    (PERSON S3)
    ; Talks
    (Talk T1)
    (Talk T2)
    (Talk T3)
    (Talk T4)
    (Talk T5)
    (Talk T6)
    ; Lunch groups
    (GROUP G1)
    (GROUP G2)
    
    ;; Declaration of the predicates of the objects
    ; We set people locations
    (is-person-at A1 R1)
    (is-person-at A2 R2)
    (is-person-at A3 R3)
    (is-person-at S1 R4)
    (is-person-at S2 R2)
    (is-person-at S3 R6)
   
    ; We set the rooms where talks take place
    (IS-TALK-AT T1 R6)
    (IS-TALK-AT T2 R5)
    (IS-TALK-AT T3 R3)
    (IS-TALK-AT T4 R4)
    (IS-TALK-AT T5 R4)
    (IS-TALK-AT T6 R1)
    
    ; We set whether the talk is a morning or afternoon talk
    (IS-MORNING T1)
    (IS-MORNING T3)
    (IS-MORNING T4)
    (IS-AFTERNOON T2)
    (IS-AFTERNOON T5)
    (IS-AFTERNOON T6)

    ; We set whether the room has catering
    (HAS-CATERING R5)
    (HAS-CATERING R6)
    
    ; We check in which lunch-group the person is
    (IS-IN-GROUP A2 G1)
    (IS-IN-GROUP S1 G1)
    (IS-IN-GROUP S3 G1)
    (IS-IN-GROUP A1 G2)
    (IS-IN-GROUP A3 G2)
    (IS-IN-GROUP S2 G2)
    
    ; We check in which room the lunch-group is placed
    (IS-GROUP-AT G1 R5)
    (IS-GROUP-AT G2 R6)

    ; We set whether the person is a speaker or an attendee
    (IS-SPEAKER S1)
    (IS-SPEAKER S2)
    (IS-SPEAKER S3)
    (IS-ATTENDEE A1)
    (IS-ATTENDEE A2)
    (IS-ATTENDEE A3)

    ; We set which speaker gives which talk
    (gives-talk S1 T1)
    (gives-talk S1 T3)
    (gives-talk S2 T2)
    (gives-talk S2 T4)
    (gives-talk S3 T5)
    (gives-talk S3 T6)
    
    ; We set the connections between the rooms
    (IS-CONNECTED R1 R2) (IS-CONNECTED R2 R1) 
    (IS-CONNECTED R2 R3) (IS-CONNECTED R3 R2) 
    (IS-CONNECTED R3 R4) (IS-CONNECTED R4 R3)
    (IS-CONNECTED R2 R5) (IS-CONNECTED R5 R2)
    (IS-CONNECTED R3 R6) (IS-CONNECTED R6 R3)
  )

  ;; Goal specification
  (:goal
    (and
      (attended-talk A1 T2)
      (attended-talk A1 T3)
      (attended-talk A2 T4)
      (attended-talk A2 T5)
      (attended-talk A3 T1)
      (attended-talk A3 T6)

      (had-lunch A1)
      (had-lunch A2)
      (had-lunch A3)
      (had-lunch S1)
      (had-lunch S2)
      (had-lunch S3)
    )
  )

)
