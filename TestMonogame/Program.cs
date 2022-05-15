using System;

namespace TestMonogame
{
    public static class Program
    {
        [STAThread]
        static void Main()
        {
            using var game = new BoulderDash();
            game.Run();
        }
    }
}
