S E L E C T   T O P   ( 1 0 0 0 ) 
     h t b l t i c k e t . t i c k e t i d   a s   T i c k e t I D  ,
    h t b l t i c k e t . a s s e t i d   a s   A s s e t I D , 
    h t b l t i c k e t . t i c k e t t y p e i d   a s   T i c k e t T y p e I D ,
     t b l a s s e t s . A s s e t N a m e   a s   A s s e t N a m e , 
    t s y s A s s e t T y p e s . A s s e t T y p e n a m e   a s   A s s e t T y p e N a m e 
 F R O M   [ l a n s w e e p e r d b ] . [ d b o ] . [ h t b l t i c k e t ] 
 I N N E R   J O I N   t b l a s s e t s 
O N   h t b l t i c k e t . a s s e t i d   =   t b l a s s e t s . a s s e t i d 
 I N N E R   J O I N   t s y s A s s e t T y p e s 
 O N   t b l a s s e t s . A s s e t T y p e   =   t s y s A s s e t T y p e s . A s s e t T y p e 
 W H E R E   h t b l t i c k e t . t i c k e t i d   =   1 0 0 ; 
