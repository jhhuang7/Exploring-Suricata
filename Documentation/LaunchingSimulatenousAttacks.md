Part of this project involved launching simultaneous attacks, this can be done with the use of the first.sh and rest.sh files.
The way it works is that the first.sh acquires a file lock, to which the rest.sh waits for this file lock to be given up before commencing.

So run first.sh, edited to have the commands you want to run after the flock in one terminal

Then rest.sh, edited to have the commands you want to after the flock in all the other terminals.

Press enter in the first.sh terminal, the file lock should release and all commands should acquire as simultaneous as you can get on this machine.

