# Interactive job
srun --partition interactive --job-name "InteractiveJob" --cpus-per-task 1 --mem-per-cpu 1G --time 2:00:00 --pty bash

# Interactive job + jupyter
srun --partition interactive --job-name "InteractiveJob" --cpus-per-task 1 --mem-per-cpu 1G --time 2:00:00 --pty --x11 --tunnel 8888:8888 bash
jupyter notebook NOTEBOOKFILE --port=8888 --browser='none'