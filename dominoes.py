from random import shuffle


class Domino:
    domino_set = []

    @classmethod
    def generate_domino_set(cls):
        Domino.domino_set = [[i, j] for i in range(7) for j in range(i, 7)]

    def __init__(self):
        self.stock = []
        self.computer = []
        self.player = []
        self.snake = []
        self.status = ''

        if not Domino.domino_set:
            Domino.generate_domino_set()

        self.shuffle()

    def __str__(self):
        return '=' * 70 \
               + '\nStock: ' + str(self.stock) \
               + '\nComputer: ' + str(self.computer) \
               + '\nSnake:' + str(self.snake) \
               + '\nPlayer: ' + str(self.player) \
               + '\n' + '=' * 70

    def shuffle(self):
        self.status = ''
        while self.status == '':
            shuffled_set = Domino.domino_set[:]
            shuffle(shuffled_set)

            self.computer = shuffled_set[:7]
            self.player = sorted(shuffled_set[7:14])
            self.stock = shuffled_set[14:]

            double_computer = max([x for x in self.computer if x[0] == x[1]], default=[])
            double_player = max([x for x in self.player if x[0] == x[1]], default=[])
            if double_computer or double_player:
                if double_computer > double_player:
                    self.computer.remove(double_computer)
                    self.snake.append(double_computer)
                    self.status = 'player'
                else:
                    self.player.remove(double_player)
                    self.snake.append(double_player)
                    self.status = 'computer'

    def print_status(self):
        status = '=' * 70 \
                 + '\nStock size: ' + str(len(self.stock)) \
                 + '\nComputer pieces: ' + str(len(self.computer)) \
                 + '\n\n'

        if len(self.snake) < 7:
            status += ' '.join([str(elem) for elem in self.snake])
        else:
            status += ' '.join([str(elem) for elem in self.snake[:3]]) + '...' \
                      + ' '.join([str(elem) for elem in self.snake[-3:]])

        status += '\n\nYour pieces:\n'

        for i in range(len(self.player)):
            status += str(i + 1) + ':' + str(self.player[i]) + '\n'

        print(status)

    def comp_move(self):

        flat = [x for sublist in self.snake for x in sublist] + [x for sublist in self.computer for x in sublist]
        numbers = [flat.count(i) for i in range(7)]
        rating = [[numbers[self.computer[i][0]] + numbers[self.computer[i][1]], self.computer[i]]
                  for i in range(len(self.computer))]
        rating.sort(reverse=True)

        first = self.snake[0][0]
        last = self.snake[-1][-1]

        for el in rating:
            chosen = el[1]
            if chosen[0] == first:
                self.computer.remove(chosen)
                self.snake.insert(0, chosen[::-1])
                break
            elif chosen[1] == first:
                self.computer.remove(chosen)
                self.snake.insert(0, chosen)
                break
            elif chosen[0] == last:
                self.computer.remove(chosen)
                self.snake.append(chosen)
                break
            elif chosen[1] == last:
                self.computer.remove(chosen)
                self.snake.append(chosen[::-1])
                break

        else:
            if self.stock:
                self.computer.append(self.stock.pop())

    def attempt_player(self, entry):
        if entry == 0:
            if self.stock:
                self.player.append(self.stock.pop())
            return True

        first = self.snake[0][0]
        last = self.snake[-1][-1]
        chosen = self.player[abs(entry) - 1]

        if (entry < 0 and chosen[0] != first and chosen[1] != first) or \
                (entry > 0 and chosen[0] != last and chosen[1] != last):
            return False

        self.player.pop(abs(entry) - 1)
        if entry < 0:
            if chosen[1] == self.snake[0][0]:
                self.snake.insert(0, chosen)
            else:
                self.snake.insert(0, chosen[::-1])

        if entry > 0:
            if chosen[0] == self.snake[-1][-1]:
                self.snake.append(chosen)
            else:
                self.snake.append(chosen[::-1])

        return True

    def change_status(self):
        self.status = 'player' if self.status == 'computer' else 'computer'

    def turn(self):
        self.print_status()

        if self.status == 'computer':
            print('Status: Computer is about to make a move. Press Enter to continue...')
            input()
            self.comp_move()
            self.change_status()
        else:
            entry = input('Status: It\'s your turn to make a move. Enter your command.\n')
            while True:
                try:
                    entry = int(entry)
                    if entry not in range(-len(self.player), len(self.player) + 1):
                        raise ValueError

                    if self.attempt_player(entry):
                        self.change_status()
                        break
                    else:
                        entry = input('\nIllegal move. Please try again.\n')

                except ValueError:
                    entry = input('\nInvalid input. Please try again.\n')

    def end_of_game(self):
        result = 'no'
        if len(self.computer) == 0:
            result = 'computer'
        elif len(self.player) == 0:
            result = 'player'
        else:
            flat = [x for sublist in self.snake for x in sublist]
            if ((flat[0] == flat[-1] or flat[0] == flat[-2]) and flat.count(flat[0]) == 8) or (
                    (flat[0] == flat[-1] or flat[0] == flat[-2]) and flat.count(flat[0]) == 8):
                result = 'draw'

        return result

    def start(self):
        end = 'no'
        while end == 'no':
            self.turn()
            end = self.end_of_game()

        self.print_status()
        if end == 'computer':
            print('Status: The game is over. The computer won!')
        elif end == 'player':
            print('Status: The game is over. You won!')
        else:
            print('Status: The game is over. It\'s a draw!')


game = Domino()
game.start()
