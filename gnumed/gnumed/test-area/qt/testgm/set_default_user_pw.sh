echo
echo "Need to change user and password in main.cpp generated by qmake."
echo
read -p "Enter postgres user: " user
read -p "enter user's password " pass


sed s/sjtan/$user/g main.cpp > main.cpp.1

sed s/pg/$pass/g main.cpp.1 > main.cpp.2


read -p "Hit Enter to see changed main.cpp:"

cat main.cpp.2

read -p " CHANGE main.cpp (Y/N)?" answ

case   $answ in y | Y ) echo "changing ...";cp main.cpp main.cpp.orig;cp main.cpp.2 main.cpp;;
*) echo "main cpp not changed";;	
esac
rm main.cpp.1
rm main.cpp.2

