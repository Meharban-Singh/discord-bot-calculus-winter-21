help = "**List of commands available**\n\n$hello OR $hi -> Greetings! :)\n$help OR $commands -> Bring this text up again\n$theorems OR $proofs OR $$definitions OR $def -> list all theorems taught so far in the course\n$theorem num OR $th num OR $proof num -> Provides solution of theorem number 'num'\n$maths OR $mathshelp OR =maths OR =mathshelp -> maths help\n$anime X Y -> searches the anime/manga/character Y. X is the type of search (`anime` or `character` or `manga`), and Y is the search query. Example: `$anime anime Attack on titan`, `$anime character levi`  \n$legends -> List all LEGENDS of the server\n\nFeedback? Use `$feedback` command"

maths = [
	['=simplify 2^2+2(2)   ', '8'],
	['=factor x^2+2x       ', 'x (x + 2)'],
	['=derive x^2+2x       ', '2 x + 2'],
	['=integrate x^2+2x    ', '1/3 x^3 + x^2 + C'],
	['=zeros x^2+2x        ', '[-2, 0]'],
	['=tangent 2lx^3       ', '12 x + -16'],
	['=area 2:4lx^3        ', '60'],
	['=cos pi                     ', '-1'],
	['=sin pi/2                   ', '1'],
	['=tan 0                      ', '0'],
	['=arccos 1                   ', '0'],
	['=arcsin 0                   ', '0'],
	['=arctan 0                   ', '0'],
	['=abs -1                     ', '1'],
	['=log 2l8                    ', '3'],
]

LEGEND_BREAKPOINT = 200
