using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net;
using System.Net.Sockets;

namespace client
{
    public partial class Form1 : Form
    {
        int port_num;
        string message;
        int byteCount;
        NetworkStream stream;
        byte[] sendData;
        byte[] getData;
        TcpClient client;

        public Form1()
        {
            InitializeComponent();
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }


        private void button1_Click(object sender, EventArgs e)
        {
            try
            {
                message = tbMessage.Text;
                byteCount = Encoding.UTF8.GetByteCount(message);
                sendData = new byte[byteCount];
                sendData = Encoding.UTF8.GetBytes(message);
                stream = client.GetStream();
                stream.Write(sendData, 0, sendData.Length);
                listBox1.Items.Add("- " + message);
            }
            catch (System.NullReferenceException)
            {
                MessageBox.Show("Отправка не удалась");
                listBox1.Items.Add("Отправка не удалась");
            }
        }

        private void button3_Click(object sender, EventArgs e)
        {
            if (!int.TryParse(tbPort.Text, out port_num))
            {
                MessageBox.Show("Неверный порт");
            }
            try
            {
                client = new TcpClient(tbIP.Text, port_num);
                MessageBox.Show("Соединение установлено");
            }
            catch (System.Net.Sockets.SocketException)
            {
                MessageBox.Show("Соединение не установлено");
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            try
            {
                getData = new byte[1024];
                stream = client.GetStream();
                int num_of_read = stream.Read(getData, 0, 1024);

                listBox1.Items.Add("- " + Encoding.UTF8.GetString(getData, 0, num_of_read));
            }
            catch (System.NullReferenceException)
            {
                MessageBox.Show("Отправка не удалась");
                listBox1.Items.Add("Отправка не удалась");
            }
        }

        private void button4_Click(object sender, EventArgs e)
        {
            stream.Close();
            client.Close();
            listBox1.Items.Add("Соединение закрыто");
        }
    }
}
