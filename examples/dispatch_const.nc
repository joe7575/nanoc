// inline dispatch with constants, any order, gaps

const IDLE = 0
const RUN = 1
const ERROR = 3

func show(int32 state) {
    dispatch(state) {
        ERROR: printf("%d: error\n", state)
        IDLE: printf("%d: idle\n", state)
        RUN: {
            printf("%d: running\n", state)
        }
    }
}

int32 i = 0
for i = 0 to 4 {
    show(i)
}
printf("done\n")
