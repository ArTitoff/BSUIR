#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>

void end() {
    printf("Process with PID %d and Parent PID %d ends.\n", getpid(), getppid());
    exit(0);
}

int main() {
    pid_t parent_pid = getppid();
    printf("Parent PID of the main process: %d\n", parent_pid);
    printf("PID of main process: %d\n", getpid());

    pid_t pid1 = fork();
    if (pid1 < 0) {
        perror("Fork failed");
        exit(1);
    }

    if (pid1 == 0) { // First child process
        printf("PID of child 1: %d\n", getpid());
        printf("Parent PID of child 1: %d\n", getppid());

        pid_t pid2 = fork();
        if (pid2 < 0) {
            perror("Fork failed");
            exit(1);
        }

        if (pid2 == 0) { // Second child process
            printf("PID of child 2: %d\n", getpid());
            printf("Parent PID of child 2: %d\n", getppid());

            pid_t pid4 = fork();
            if (pid4 < 0) {
                perror("Fork failed");
                exit(1);
            }

            if (pid4 == 0) { // Third child (5th in the tree)
                printf("PID of child 4: %d\n", getpid());
                printf("Parent PID of child 4: %d\n", getppid());
                end();
            }
            end();
        }

        pid_t pid3 = fork();
        if (pid3 < 0) {
            perror("Fork failed");
            exit(1);
        }

        if (pid3 == 0) { // Third child process (Fourth in the tree)
            printf("PID of child 3: %d\n", getpid());
            printf("Parent PID of child 3: %d\n", getppid());

            pid_t pid5 = fork();
            if (pid5 < 0) {
                perror("Fork failed");
                exit(1);
            }

            if (pid5 == 0) { // Fourth child (6th in the tree)
                printf("PID of child 5: %d\n", getpid());
                printf("Parent PID of child 5: %d\n", getppid());

                pid_t pid6 = fork();
                if (pid6 < 0) {
                    perror("Fork failed");
                    exit(1);
                }

                if (pid6 == 0) { // Fifth child (7th in the tree)
                    printf("PID of child 6: %d\n", getpid());
                    printf("Parent PID of child 6: %d\n", getppid());
                    end();
                }
                end();
            }
            end();
        }
    }

    // Execute the command 'ps' in the parent process
    char *args[] = {"ps", NULL};
    execvp(args[0], args);
    perror("execvp failed"); // Only reached if execvp fails
    end(); // If exec fails, we end the parent

    // Parent waits for all children to finish
    while (wait(NULL) > 0);

    printf("Main process ends.\n");
    return 0;
}
