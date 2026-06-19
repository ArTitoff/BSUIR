#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
void end(){
    printf("Procces with PID %d and Parent Pid %d end.\n", getpid(), getppid()); exit(0);
}
int main() {
   pid_t parent_pid = getppid();
    printf("RoditelPID1: %d\n", parent_pid);



  pid_t pid1 = fork();
  if (pid1 == 0){
      printf("PID2: %d\n", getpid());
      printf("RoditelllllllPID2: %d\n", getppid());
    pid_t pid2 = fork();
      if (pid2 == 0){
          printf("PID3: %d\n", getpid());
          printf("RoditelllllllPID3: %d\n", getppid());
         pid_t pid4 = fork();
          if (pid4 == 0){
              printf("PID5: %d\n", getpid());
              printf("RoditelllllllPID5: %d\n", getppid());
              end();
  }
 	end();
      }
     else if (pid2 > 0) {
        // Код родительского процесса
        wait(NULL); // Ожидание завершения дочернего процесса  
    }
      
 pid_t pid3 = fork();
  if (pid3 == 0){
      printf("PID4: %d\n", getpid());
      printf("RoditelllllllPID4: %d\n", getppid());
	 
      pid_t pid5 = fork();
      if (pid5 == 0){
          printf("PID6: %d\n", getpid());
          printf("RoditelllllllPID6: %d\n", getppid());
         pid_t pid6 = fork();
         
          if (pid6 == 0){
              printf("PID7: %d\n", getpid());
              printf("RoditelllllllPID7: %d\n", getppid());
              end();
          } 
           end();       
      }
        else if (pid5 > 0) {
        // Код родительского процесса
        wait(NULL); // Ожидание завершения дочернего процесса
       
    }
    end();
  }
    else if (pid3 > 0) {
        // Код родительского процесса
        wait(NULL); // Ожидание завершения дочернего процесса
        
    }
    end();
  char *args[] = {"ps", NULL};
  execvp(args[0], args);
    



    }
    else if (pid1 > 0) {
        // Код родительского процесса
        wait(NULL); // Ожидание завершения дочернего процесса
       
    }
    printf("PID0: %d\n", getpid());

}

