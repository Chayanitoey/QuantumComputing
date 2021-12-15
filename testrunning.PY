{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#reference\n",
    "#https://github.com/JRussellHuffman/Rothko-Bell/blob/main/Bell%20Art.ipynb\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "##reference\n",
    "##https://github.com/qiskit-community/qiskit-community-tutorials/blob/master/Coding_With_Qiskit/ep5_Quantum_Teleportation.ipynb\n",
    "\n",
    "from qiskit import * \n",
    "from qiskit import IBMQ\n",
    "from qiskit.visualization import plot_histogram\n",
    "from qiskit.tools.monitor import job_monitor\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "ibmqfactory.load_account:WARNING:2021-10-07 16:44:02,367: Credentials are already in use. The existing account in the session will be replaced.\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "[<IBMQSimulator('ibmq_qasm_simulator') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQBackend('ibmq_armonk') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQBackend('ibmq_santiago') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQBackend('ibmq_bogota') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQBackend('ibmq_lima') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQBackend('ibmq_belem') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQBackend('ibmq_quito') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQSimulator('simulator_statevector') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQSimulator('simulator_mps') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQSimulator('simulator_extended_stabilizer') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQSimulator('simulator_stabilizer') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQBackend('ibmq_manila') from IBMQ(hub='ibm-q', group='open', project='main')>]"
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "IBMQ.providers()\n",
    "IBMQ.load_account()\n",
    "provider = IBMQ.get_provider(hub='ibm-q')\n",
    "provider.backends()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<pre style=\"word-wrap: normal;white-space: pre;background: #fff0;line-height: 1.1;font-family: &quot;Courier New&quot;,Courier,monospace\">     ┌───┐┌─┐      \n",
       "q_0: ┤ H ├┤M├──────\n",
       "     ├───┤└╥┘┌─┐   \n",
       "q_1: ┤ H ├─╫─┤M├───\n",
       "     ├───┤ ║ └╥┘┌─┐\n",
       "q_2: ┤ H ├─╫──╫─┤M├\n",
       "     └───┘ ║  ║ └╥┘\n",
       "c: 3/══════╩══╩══╩═\n",
       "           0  1  2 </pre>"
      ],
      "text/plain": [
       "     ┌───┐┌─┐      \n",
       "q_0: ┤ H ├┤M├──────\n",
       "     ├───┤└╥┘┌─┐   \n",
       "q_1: ┤ H ├─╫─┤M├───\n",
       "     ├───┤ ║ └╥┘┌─┐\n",
       "q_2: ┤ H ├─╫──╫─┤M├\n",
       "     └───┘ ║  ║ └╥┘\n",
       "c: 3/══════╩══╩══╩═\n",
       "           0  1  2 "
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "circuit = QuantumCircuit(3,3)\n",
    "# ========================\n",
    "# Step 0: Create the state to be teleported in qubit 0\n",
    "circuit.h(0)\n",
    "circuit.h(1)\n",
    "circuit.h(2)\n",
    "\n",
    "\n",
    "circuit.measure([0, 1, 2], [0, 1, 2]) \n",
    "circuit.draw()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAc0AAAFDCAYAAABY/1W1AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAADh0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uMy4xLjMsIGh0dHA6Ly9tYXRwbG90bGliLm9yZy+AADFEAAAgAElEQVR4nO3deZwU1dX/8c8RZIQfGFkEHAYEZBEGAccxOBFBYwj+8CcJiaImxigqauKCS6J5XJNojEsWEx81j0twiWIkiVsUMfGBAUVkEQwQhSioKItsAQyCDOf3x60Zm6FnqGZ6Zb7v12tedFdVF6eme/pU3br3XHN3REREZPf2yXUAIiIihUJJU0REJCYlTRERkZiUNEVERGJS0hQREYlJSVNERCSmprkOIJfatWvnXbt2zXUYIiKSR+bMmbPG3Q9Mtq5RJ82uXbsye/bsXIchIiJ5xMzeq2udmmdFRERiUtIUERGJSUlTREQkJiVNERGRmJQ0RUREYlLSFBERiUlJU0REJCYlTRERkZiUNEVERGJS0hQREYkp60nTzL5nZkvN7FMzm2Nmx9Sz7UFm9piZvWVmVWY2vo7t9jez35jZR2a21cz+ZWajM3YQIiLSKGU1aZrZqcCdwM+Aw4FXgRfMrEsdLykC1gA/B2bWsc99gclAT2A00Bs4C1iazthFRESyXbD9cmC8u98XPb/YzE4ALgR+VHtjd18GXAJgZifXsc+zgfbAEHffFi1blsaYRUREgCxeaZpZM+AIwlVhosnAlxqw668DrwC/NbOVZrbIzG6MrkBFRETSJptXmu2AJsCqWstXAV9pwH67A18GHgNOBLoC/w20BK6svbGZjQXGAhQXFzNlypSwk+7dadWqFfPnzwegbdu2lJaWUllZCUDTpk0ZPHgwc+fOZePGjQCUl5ezatUqPvjgAwB69uxJUVERCxYsAKB9+/b06tWL6dOnA1BUVERFRQWzZ89m8+bNAAwaNIjly5fz4YcfAtC7d2+aNGnCokWLAOjYsSPdunVjxowZADRv3pxBgwYxc+ZMtmzZAkBFRQVLly5l5cqVAPTt25eqqirefvttADp16kRJSQkzZ4YW7pYtW1JeXs6MGTPYunUrAIMHD2bx4sWsXr0agH79+rF161aWLFkCQOfOnenQoUPNVGr7778/ZWVlTJ8+ne3btwMwZMgQFi5cyNq1awEYMGAAmzZt4t133wXCVGxt2rRh7ty5ALRu3ZoBAwYwdepU3B0zY+jQocyfP5/169cDUFZWxrp161i2bJneJ71Pep/0PmXlfaqPuXu9G6SLmRUDHxKaUaclLL8BON3dD93N658D1rj7WbWWLwb2A7q5e1W0bCzwK6Cl13OA5eXlrvk0RUQkkZnNcffyZOuyeaW5BqgCOtZa3p5drz5TsQL4rDphRv4JtCBc3X7cgH2LiIjUyNo9zaiTzhxgWK1Vwwi9aPfUK0APM0s8ll7AfwiJWkREJC2yPU7zl8BZZnaumfUxszuBYuBeADN72MweTnyBmQ00s4HA/kCb6HnfhE3uAdoAd5pZbzMbDvwYuLu+plkREZFUZXXIibs/YWZtgWuBg4AFwAh3fy/aJNl4zTdqPT8JeI/Q4Qd3/8DMvkpIyPOAlcCDwE1pPwAREWnUsj1OE3e/G7i7jnXHJllmMfb5Gg0btiIiIrJbqj0rIiISk5KmSA5MmjSJ3r1706NHD37+85/vsr6yspKysjKaNm3KxIkTd1m/ceNGOnXqxEUXXQTAf/7zH0488UQOPfRQSktLufrqqzN+DCKNkZKmSJZVVVXx/e9/nxdeeIFFixbx+OOP1wzqrtalSxfGjx/Pt771raT7uO666xg6dOhOy6688kreeust3njjDV555RVeeOGFjB2DSGOlpCmSZa+//jo9evSge/fuNGvWjNNOO42nn356p226du1K//792WefXf9E58yZw6pVq/jqV79as6xFixYcd9xxADRr1oyysjKWL1+e2QMRaYSUNEWy7MMPP6Rz5841z0tKSmrKie3Ojh07uOKKK7j99tvr3GbDhg08++yzHH/88Q2OVUR2pqQpkmXJhg+b7baTOAB33303I0aM2CnpJtq+fTunn346l1xyCd27d29QnCKyq6wPORFp7EpKSmqKXQMsX76c4uLiWK+dMWMG06ZN4+6772bz5s1s27aNli1b1nQmGjt2LD179mTcuHEZiV2ksVPSFMmyI488kiVLlrB06VI6derEhAkTeOyxx2K99g9/+EPN4/HjxzN79uyahHnttdfy73//m/vvvz8jcYuImmdFsq5p06bcddddDB8+nD59+jB69GhKS0u5/vrreeaZZwCYNWsWJSUlPPnkk5x//vmUlpbWu8/ly5dz8803s2jRIsrKyhg4cKCSp0gGZG1qsHykqcFERKS2+qYG05WmiIhITEqaIiKSFXtaCeu9997jiCOOYODAgZSWlnLvvffWrNu2bRtjx46lV69eHHroofzpT3/K6DGoI5CIiGRcdSWsl156iZKSEo488khGjhxJ376fz/RYXQnrjjvu2Om1Bx10EK+++ipFRUVs3ryZfv36MXLkSIqLi7n55ptp3749ixcvZseOHaxbty6jx6GkKSIiGZdYCQuoqYSVmDS7du0KsEslrGbNmtU83rp1Kzt27Kh5/uCDD/LWW2/VvK5du3aZOoTwf2R07yIiIjSsEhbABx98QP/+/encuTNXXXUVxcXFbNiwAQi1mMvKyjjllFNYtWpV2mNPpKQpIiIZ15BKWACdO3fmzTff5F//+hcPPfQQq1atYvv27Sxfvpyjjz6auXPnUlFRwZVXXpnOsHehpCkiIhnXkEpYiYqLiyktLWXatGm0bduWFi1aMGrUKABOOeUU5s6dm7aYk1HSFBGRjEushLVt2zYmTJjAyJEjY712+fLlbNmyBYD169fzyiuv0Lt3b8yMk046iSlTpgDw97//fad7pJmg4gYqbiAikhXPP/8848aNo6qqijFjxnDNNddw/fXXU15ezsiRI5k1axajRo1i/fr17LfffnTs2JGFCxfy0ksvccUVV2BmuDsXXXQRY8eOBcJwlO985zts2LCBAw88kN///vd06dKlQXHWV9xASVNJU0REEqgikIiISBooaYqIiMSk4gaN2KRJk7j00kupqqri3HPP5eqrr95pfWVlJePGjePNN99kwoQJnHzyyQDMmzePCy+8kI0bN9KkSROuueYaTj31VABefvllrrzySrZt28YRRxzBAw88QNOmmfmYFXr85/06I7utcZ+m1BRJO11pNlLVJa1eeOEFFi1axOOPP86iRYt22qa6pNW3vvWtnZa3aNGChx9+mIULFzJp0iTGjRvHhg0b2LFjB9/97neZMGECCxYs4OCDD+ahhx5S/CKy11DSbKQSS1o1a9aspqRVoq5du9K/f/9dSlr16tWLnj17AmHMVPv27fn4449Zu3YtRUVF9OrVC4Bhw4ZlrHhyoccvIoVJSbORamhJq2qvv/4627Zt45BDDqFdu3Z89tlnVPdInjhx4k6DmdOp0OMXkcKkpNlINbSkFcCKFSv4zne+w+9//3v2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\n",
      "text/plain": [
       "<Figure size 504x360 with 1 Axes>"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "simulator = Aer.get_backend('qasm_simulator')\n",
    "result = execute(circuit, backend=simulator, shots=1024).result()\n",
    "\n",
    "plot_histogram(result.get_counts(circuit))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[<IBMQSimulator('ibmq_qasm_simulator') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQBackend('ibmq_armonk') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQBackend('ibmq_santiago') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQBackend('ibmq_bogota') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQBackend('ibmq_lima') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQBackend('ibmq_belem') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQBackend('ibmq_quito') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQSimulator('simulator_statevector') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQSimulator('simulator_mps') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQSimulator('simulator_extended_stabilizer') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQSimulator('simulator_stabilizer') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQBackend('ibmq_manila') from IBMQ(hub='ibm-q', group='open', project='main')>]"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "qcomp = provider.get_backend('ibmq_santiago')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "615dfeae73064c5350619ee3\n",
      "Job Status: job has successfully run\n"
     ]
    }
   ],
   "source": [
    "# run the job on the backend qcomp\n",
    "job = execute(circuit, backend=qcomp, shots=8000, initial_layout=[0,1,2], memory=True)\n",
    "print(job.job_id())\n",
    "\n",
    "from qiskit.tools.monitor import job_monitor\n",
    "job_monitor(job)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "{'000': 1016,\n",
       " '001': 1040,\n",
       " '010': 1051,\n",
       " '011': 1034,\n",
       " '100': 955,\n",
       " '101': 962,\n",
       " '110': 982,\n",
       " '111': 960}"
      ]
     },
     "execution_count": 15,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "result = job.result()\n",
    "result.get_counts()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [],
   "source": [
    "myjson = result.get_memory()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## DJ Algo"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<pre style=\"word-wrap: normal;white-space: pre;background: #fff0;line-height: 1.1;font-family: &quot;Courier New&quot;,Courier,monospace\">          ┌───┐ ░ ┌───┐                ░ ┌───┐┌───┐ ░ ┌─┐      \n",
       "q_0: ─|0>─┤ H ├─░─┤ X ├──■─────────────░─┤ X ├┤ H ├─░─┤M├──────\n",
       "          ├───┤ ░ └───┘  │             ░ ├───┤└───┘ ░ └╥┘┌─┐   \n",
       "q_1: ─|0>─┤ H ├─░────────┼────■────────░─┤ H ├──────░──╫─┤M├───\n",
       "          ├───┤ ░ ┌───┐  │    │        ░ ├───┤┌───┐ ░  ║ └╥┘┌─┐\n",
       "q_2: ─|0>─┤ H ├─░─┤ X ├──┼────┼────■───░─┤ X ├┤ H ├─░──╫──╫─┤M├\n",
       "     ┌───┐├───┤ ░ └───┘┌─┴─┐┌─┴─┐┌─┴─┐ ░ └───┘└───┘ ░  ║  ║ └╥┘\n",
       "q_3: ┤ X ├┤ H ├─░──────┤ X ├┤ X ├┤ X ├─░────────────░──╫──╫──╫─\n",
       "     └───┘└───┘ ░      └───┘└───┘└───┘ ░            ░  ║  ║  ║ \n",
       "c: 4/══════════════════════════════════════════════════╩══╩══╩═\n",
       "                                                       0  1  2 </pre>"
      ],
      "text/plain": [
       "          ┌───┐ ░ ┌───┐                ░ ┌───┐┌───┐ ░ ┌─┐      \n",
       "q_0: ─|0>─┤ H ├─░─┤ X ├──■─────────────░─┤ X ├┤ H ├─░─┤M├──────\n",
       "          ├───┤ ░ └───┘  │             ░ ├───┤└───┘ ░ └╥┘┌─┐   \n",
       "q_1: ─|0>─┤ H ├─░────────┼────■────────░─┤ H ├──────░──╫─┤M├───\n",
       "          ├───┤ ░ ┌───┐  │    │        ░ ├───┤┌───┐ ░  ║ └╥┘┌─┐\n",
       "q_2: ─|0>─┤ H ├─░─┤ X ├──┼────┼────■───░─┤ X ├┤ H ├─░──╫──╫─┤M├\n",
       "     ┌───┐├───┤ ░ └───┘┌─┴─┐┌─┴─┐┌─┴─┐ ░ └───┘└───┘ ░  ║  ║ └╥┘\n",
       "q_3: ┤ X ├┤ H ├─░──────┤ X ├┤ X ├┤ X ├─░────────────░──╫──╫──╫─\n",
       "     └───┘└───┘ ░      └───┘└───┘└───┘ ░            ░  ║  ║  ║ \n",
       "c: 4/══════════════════════════════════════════════════╩══╩══╩═\n",
       "                                                       0  1  2 "
      ]
     },
     "execution_count": 25,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# qreg_q = QuantumRegister(4, 'q')\n",
    "# creg_c = ClassicalRegister(4, 'c')\n",
    "circuit = QuantumCircuit(4,4)\n",
    "\n",
    "circuit.reset(qreg_q[0])\n",
    "circuit.reset(qreg_q[1])\n",
    "circuit.reset(qreg_q[2])\n",
    "circuit.x(qreg_q[3])\n",
    "circuit.h(qreg_q[0])\n",
    "circuit.h(qreg_q[1])\n",
    "circuit.h(qreg_q[2])\n",
    "circuit.h(qreg_q[3])\n",
    "circuit.barrier()\n",
    "\n",
    "circuit.x(qreg_q[0])\n",
    "circuit.x(qreg_q[2])\n",
    "circuit.cx(qreg_q[0], qreg_q[3])\n",
    "circuit.cx(qreg_q[1], qreg_q[3])\n",
    "circuit.cx(qreg_q[2], qreg_q[3])\n",
    "\n",
    "circuit.barrier()\n",
    "\n",
    "circuit.x(qreg_q[0])\n",
    "circuit.h(qreg_q[0])\n",
    "circuit.h(qreg_q[1])\n",
    "circuit.x(qreg_q[2])\n",
    "circuit.h(qreg_q[2])\n",
    "\n",
    "circuit.barrier()\n",
    "\n",
    "circuit.measure(qreg_q[0], creg_c[0])\n",
    "circuit.measure(qreg_q[1], creg_c[1])\n",
    "circuit.measure(qreg_q[2], creg_c[2])\n",
    "\n",
    "circuit.draw()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 504x360 with 1 Axes>"
      ]
     },
     "execution_count": 26,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "simulator = Aer.get_backend('qasm_simulator')\n",
    "result = execute(circuit, backend=simulator, shots=1024).result()\n",
    "from qiskit.visualization import plot_histogram\n",
    "plot_histogram(result.get_counts(circuit))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "615e1122059e1b0d96a66a2e\n",
      "Job Status: job has successfully run\n"
     ]
    }
   ],
   "source": [
    "qcomp = provider.get_backend('ibmq_santiago')\n",
    "\n",
    "# run the job on the backend qcomp\n",
    "job = execute(circuit, backend=qcomp, shots=8000, initial_layout=[0,1,2,3], memory=True)\n",
    "print(job.job_id())\n",
    "\n",
    "job_monitor(job)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 29,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "{'0000': 143,\n",
       " '0001': 243,\n",
       " '0010': 77,\n",
       " '0011': 538,\n",
       " '0100': 140,\n",
       " '0101': 1593,\n",
       " '0110': 251,\n",
       " '0111': 5015}"
      ]
     },
     "execution_count": 29,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "result = job.result()\n",
    "result.get_counts()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "metadata": {},
   "outputs": [],
   "source": [
    "myjson = result.get_memory()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 111 real"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [
    {
     "ename": "CircuitError",
     "evalue": "'qargs not in this circuit'",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mCircuitError\u001b[0m                              Traceback (most recent call last)",
      "\u001b[0;32m<ipython-input-19-820840241d82>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m      3\u001b[0m \u001b[0mcircuit\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mQuantumCircuit\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;36m3\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;36m3\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      4\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 5\u001b[0;31m \u001b[0mcircuit\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mreset\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mqreg_q\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;36m0\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      6\u001b[0m \u001b[0mcircuit\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mreset\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mqreg_q\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;36m1\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      7\u001b[0m \u001b[0mcircuit\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mreset\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mqreg_q\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;36m2\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m/opt/miniconda3/lib/python3.7/site-packages/qiskit/circuit/reset.py\u001b[0m in \u001b[0;36mreset\u001b[0;34m(self, qubit)\u001b[0m\n\u001b[1;32m     32\u001b[0m \u001b[0;32mdef\u001b[0m \u001b[0mreset\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mqubit\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     33\u001b[0m     \u001b[0;34m\"\"\"Reset q.\"\"\"\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 34\u001b[0;31m     \u001b[0;32mreturn\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mappend\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mReset\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m[\u001b[0m\u001b[0mqubit\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m[\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     35\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     36\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m/opt/miniconda3/lib/python3.7/site-packages/qiskit/circuit/quantumcircuit.py\u001b[0m in \u001b[0;36mappend\u001b[0;34m(self, instruction, qargs, cargs)\u001b[0m\n\u001b[1;32m   1084\u001b[0m         \u001b[0minstructions\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mInstructionSet\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   1085\u001b[0m         \u001b[0;32mfor\u001b[0m \u001b[0;34m(\u001b[0m\u001b[0mqarg\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mcarg\u001b[0m\u001b[0;34m)\u001b[0m \u001b[0;32min\u001b[0m \u001b[0minstruction\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mbroadcast_arguments\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mexpanded_qargs\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mexpanded_cargs\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m-> 1086\u001b[0;31m             \u001b[0minstructions\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0madd\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_append\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0minstruction\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mqarg\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mcarg\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mqarg\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mcarg\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m   1087\u001b[0m         \u001b[0;32mreturn\u001b[0m \u001b[0minstructions\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   1088\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m/opt/miniconda3/lib/python3.7/site-packages/qiskit/circuit/quantumcircuit.py\u001b[0m in \u001b[0;36m_append\u001b[0;34m(self, instruction, qargs, cargs)\u001b[0m\n\u001b[1;32m   1108\u001b[0m         \u001b[0;31m# do some compatibility checks\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   1109\u001b[0m         \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_check_dups\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mqargs\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m-> 1110\u001b[0;31m         \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_check_qargs\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mqargs\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m   1111\u001b[0m         \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_check_cargs\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mcargs\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   1112\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m/opt/miniconda3/lib/python3.7/site-packages/qiskit/circuit/quantumcircuit.py\u001b[0m in \u001b[0;36m_check_qargs\u001b[0;34m(self, qargs)\u001b[0m\n\u001b[1;32m   1232\u001b[0m             \u001b[0;32mraise\u001b[0m \u001b[0mCircuitError\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m\"qarg is not a Qubit\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   1233\u001b[0m         \u001b[0;32mif\u001b[0m \u001b[0;32mnot\u001b[0m \u001b[0mset\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mqargs\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0missubset\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_qubit_set\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m-> 1234\u001b[0;31m             \u001b[0;32mraise\u001b[0m \u001b[0mCircuitError\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m\"qargs not in this circuit\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m   1235\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   1236\u001b[0m     \u001b[0;32mdef\u001b[0m \u001b[0m_check_cargs\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mcargs\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;31mCircuitError\u001b[0m: 'qargs not in this circuit'"
     ]
    }
   ],
   "source": [
    "qreg_q = QuantumRegister(3, 'q')\n",
    "creg_c = ClassicalRegister(3, 'c')\n",
    "circuit = QuantumCircuit(3, 3)\n",
    "\n",
    "circuit = QuantumCircuit(qreg_q, creg_c)\n",
    "\n",
    "circuit.reset(qreg_q[0])\n",
    "circuit.reset(qreg_q[1])\n",
    "circuit.reset(qreg_q[2])\n",
    "circuit.x(qreg_q[0])\n",
    "circuit.x(qreg_q[1])\n",
    "circuit.x(qreg_q[2])\n",
    "circuit.measure(qreg_q[0], creg_c[0])\n",
    "circuit.measure(qreg_q[1], creg_c[1])\n",
    "circuit.measure(qreg_q[2], creg_c[2])\n",
    "\n",
    "circuit.draw()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 504x360 with 1 Axes>"
      ]
     },
     "execution_count": 14,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "simulator = Aer.get_backend('qasm_simulator')\n",
    "result = execute(circuit, backend=simulator, shots=1024).result()\n",
    "from qiskit.visualization import plot_histogram\n",
    "plot_histogram(result.get_counts(circuit))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "615f5c57f9a6d93c2d990955\n",
      "Job Status: job has successfully run\n"
     ]
    }
   ],
   "source": [
    "qcomp = provider.get_backend('ibmq_santiago')\n",
    "\n",
    "# run the job on the backend qcomp\n",
    "job = execute(circuit, backend=qcomp, shots=8000, initial_layout=[0,1,2,3], memory=True)\n",
    "print(job.job_id())\n",
    "\n",
    "job_monitor(job)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "{'0000': 4,\n",
       " '0001': 169,\n",
       " '0010': 244,\n",
       " '0011': 7452,\n",
       " '0100': 2,\n",
       " '0101': 63,\n",
       " '0110': 1,\n",
       " '0111': 65}"
      ]
     },
     "execution_count": 16,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "result = job.result()\n",
    "result.get_counts()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [],
   "source": [
    "myjson = result.get_memory()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## second method"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 35,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<pre style=\"word-wrap: normal;white-space: pre;background: #fff0;line-height: 1.1;font-family: &quot;Courier New&quot;,Courier,monospace\">     ┌───┐ ░            ░      ┌───┐\n",
       "q_0: ┤ X ├─░────────────░───■──┤ H ├\n",
       "     └───┘ ░ ┌───┐      ░ ┌─┴─┐└───┘\n",
       "q_1: ──────░─┤ H ├──■───░─┤ X ├─────\n",
       "           ░ └───┘┌─┴─┐ ░ └───┘     \n",
       "q_2: ──────░──────┤ X ├─░───────────\n",
       "           ░      └───┘ ░           \n",
       "c: 3/═══════════════════════════════\n",
       "                                    </pre>"
      ],
      "text/plain": [
       "     ┌───┐ ░            ░      ┌───┐\n",
       "q_0: ┤ X ├─░────────────░───■──┤ H ├\n",
       "     └───┘ ░ ┌───┐      ░ ┌─┴─┐└───┘\n",
       "q_1: ──────░─┤ H ├──■───░─┤ X ├─────\n",
       "           ░ └───┘┌─┴─┐ ░ └───┘     \n",
       "q_2: ──────░──────┤ X ├─░───────────\n",
       "           ░      └───┘ ░           \n",
       "c: 3/═══════════════════════════════\n",
       "                                    "
      ]
     },
     "execution_count": 35,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "circuit.barrier() \n",
    "circuit.h(1)\n",
    "circuit.cx(1,2)\n",
    "\n",
    "circuit.barrier()\n",
    "circuit.cx(0,1)\n",
    "circuit.h(0)\n",
    "\n",
    "circuit.draw()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 36,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<pre style=\"word-wrap: normal;white-space: pre;background: #fff0;line-height: 1.1;font-family: &quot;Courier New&quot;,Courier,monospace\">     ┌───┐ ░            ░      ┌───┐ ░ ┌─┐    ░            \n",
       "q_0: ┤ X ├─░────────────░───■──┤ H ├─░─┤M├────░───────■────\n",
       "     └───┘ ░ ┌───┐      ░ ┌─┴─┐└───┘ ░ └╥┘┌─┐ ░       │    \n",
       "q_1: ──────░─┤ H ├──■───░─┤ X ├──────░──╫─┤M├─░───■───┼────\n",
       "           ░ └───┘┌─┴─┐ ░ └───┘      ░  ║ └╥┘ ░ ┌─┴─┐ │ ┌─┐\n",
       "q_2: ──────░──────┤ X ├─░────────────░──╫──╫──░─┤ X ├─■─┤M├\n",
       "           ░      └───┘ ░            ░  ║  ║  ░ └───┘   └╥┘\n",
       "c: 3/═══════════════════════════════════╩══╩═════════════╩═\n",
       "                                        0  1             2 </pre>"
      ],
      "text/plain": [
       "     ┌───┐ ░            ░      ┌───┐ ░ ┌─┐    ░            \n",
       "q_0: ┤ X ├─░────────────░───■──┤ H ├─░─┤M├────░───────■────\n",
       "     └───┘ ░ ┌───┐      ░ ┌─┴─┐└───┘ ░ └╥┘┌─┐ ░       │    \n",
       "q_1: ──────░─┤ H ├──■───░─┤ X ├──────░──╫─┤M├─░───■───┼────\n",
       "           ░ └───┘┌─┴─┐ ░ └───┘      ░  ║ └╥┘ ░ ┌─┴─┐ │ ┌─┐\n",
       "q_2: ──────░──────┤ X ├─░────────────░──╫──╫──░─┤ X ├─■─┤M├\n",
       "           ░      └───┘ ░            ░  ║  ║  ░ └───┘   └╥┘\n",
       "c: 3/═══════════════════════════════════╩══╩═════════════╩═\n",
       "                                        0  1             2 "
      ]
     },
     "execution_count": 36,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "circuit.barrier()\n",
    "circuit.measure([0, 1], [0, 1]) \n",
    "circuit.barrier()\n",
    "circuit.cx(1, 2)\n",
    "circuit.cz(0, 2)\n",
    "circuit.measure([2], [2])\n",
    "\n",
    "circuit.draw()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 37,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 504x360 with 1 Axes>"
      ]
     },
     "execution_count": 37,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "\n",
    "simulator = Aer.get_backend('qasm_simulator')\n",
    "result = execute(circuit, backend=simulator, shots=1024).result()\n",
    "from qiskit.visualization import plot_histogram\n",
    "plot_histogram(result.get_counts(circuit))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 38,
   "metadata": {},
   "outputs": [],
   "source": [
    "from qiskit import IBMQ"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "configrc.store_credentials:WARNING:2021-10-04 16:55:11,472: Credentials already present. Set overwrite=True to overwrite.\n"
     ]
    }
   ],
   "source": [
    "IBMQ.save_account('98bc6351eb3afe9150711f1220dd7ce9179360937bf419b04b85ca0faa98bf19644721d89ae4123d8f5c97febbd91a68e64c0ffc0ca1590bde6a8c762f5a03f2')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 40,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[<AccountProvider for IBMQ(hub='ibm-q', group='open', project='main')>]"
      ]
     },
     "execution_count": 40,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "IBMQ.providers()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 41,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "ibmqfactory.load_account:WARNING:2021-10-04 16:55:20,825: Credentials are already in use. The existing account in the session will be replaced.\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "[<IBMQSimulator('ibmq_qasm_simulator') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQBackend('ibmq_armonk') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQBackend('ibmq_santiago') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQBackend('ibmq_bogota') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQBackend('ibmq_lima') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQBackend('ibmq_belem') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQBackend('ibmq_quito') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQSimulator('simulator_statevector') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQSimulator('simulator_mps') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQSimulator('simulator_extended_stabilizer') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQSimulator('simulator_stabilizer') from IBMQ(hub='ibm-q', group='open', project='main')>,\n",
       " <IBMQBackend('ibmq_manila') from IBMQ(hub='ibm-q', group='open', project='main')>]"
      ]
     },
     "execution_count": 41,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# load account\n",
    "IBMQ.load_account()\n",
    "provider = IBMQ.get_provider(hub='ibm-q')\n",
    "provider.backends()\n",
    "# qcomp = provider.get_backend('ibmq_16_melbourne')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 44,
   "metadata": {},
   "outputs": [],
   "source": [
    "qcomp = provider.get_backend('ibmq_santiago')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 45,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "615b6aef49770e26d013ff66\n",
      "Job Status: job has successfully run\n"
     ]
    }
   ],
   "source": [
    "# run the job on the backend qcomp\n",
    "job = execute(circuit, backend=qcomp, shots=512, initial_layout=[0,1,2], memory=True)\n",
    "print(job.job_id())\n",
    "\n",
    "from qiskit.tools.monitor import job_monitor\n",
    "job_monitor(job)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 48,
   "metadata": {},
   "outputs": [],
   "source": [
    "result = job.result()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 49,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Result(backend_name='ibmq_santiago', backend_version='1.3.31', qobj_id='ba775053-0f7b-47a7-82ae-ce0a42ff203c', job_id='615b6aef49770e26d013ff66', success=True, results=[ExperimentResult(shots=512, success=True, meas_level=2, data=ExperimentResultData(counts={'0x0': 72, '0x1': 61, '0x2': 51, '0x3': 61, '0x4': 78, '0x5': 54, '0x6': 67, '0x7': 68}, memory=['0x0', '0x3', '0x4', '0x4', '0x2', '0x0', '0x4', '0x0', '0x1', '0x2', '0x4', '0x4', '0x7', '0x3', '0x2', '0x5', '0x6', '0x0', '0x5', '0x4', '0x1', '0x0', '0x4', '0x4', '0x2', '0x2', '0x6', '0x3', '0x0', '0x4', '0x6', '0x1', '0x2', '0x7', '0x7', '0x1', '0x6', '0x2', '0x1', '0x5', '0x1', '0x0', '0x1', '0x0', '0x4', '0x6', '0x6', '0x1', '0x4', '0x2', '0x7', '0x7', '0x0', '0x1', '0x0', '0x7', '0x7', '0x7', '0x0', '0x2', '0x0', '0x7', '0x6', '0x6', '0x1', '0x2', '0x5', '0x2', '0x5', '0x4', '0x7', '0x7', '0x1', '0x0', '0x2', '0x6', '0x6', '0x7', '0x1', '0x3', '0x5', '0x7', '0x7', '0x0', '0x5', '0x2', '0x7', '0x7', '0x7', '0x7', '0x1', '0x0', '0x3', '0x7', '0x5', '0x5', '0x0', '0x6', '0x7', '0x4', '0x0', '0x6', '0x7', '0x5', '0x6', '0x4', '0x4', '0x1', '0x0', '0x3', '0x2', '0x0', '0x6', '0x4', '0x5', '0x6', '0x2', '0x3', '0x6', '0x6', '0x0', '0x0', '0x1', '0x1', '0x0', '0x7', '0x3', '0x3', '0x5', '0x1', '0x2', '0x0', '0x4', '0x6', '0x3', '0x6', '0x2', '0x1', '0x7', '0x3', '0x2', '0x5', '0x6', '0x7', '0x5', '0x3', '0x6', '0x1', '0x6', '0x4', '0x6', '0x0', '0x7', '0x6', '0x5', '0x0', '0x7', '0x2', '0x0', '0x5', '0x1', '0x1', '0x2', '0x7', '0x3', '0x7', '0x2', '0x5', '0x7', '0x5', '0x6', '0x0', '0x6', '0x3', '0x3', '0x5', '0x3', '0x4', '0x5', '0x7', '0x0', '0x0', '0x1', '0x1', '0x4', '0x1', '0x7', '0x1', '0x6', '0x2', '0x2', '0x0', '0x0', '0x7', '0x4', '0x4', '0x0', '0x7', '0x5', '0x2', '0x0', '0x4', '0x0', '0x4', '0x2', '0x6', '0x4', '0x4', '0x5', '0x3', '0x4', '0x3', '0x2', '0x1', '0x4', '0x4', '0x1', '0x6', '0x1', '0x4', '0x3', '0x0', '0x0', '0x0', '0x2', '0x7', '0x7', '0x3', '0x4', '0x2', '0x0', '0x1', '0x3', '0x1', '0x5', '0x0', '0x2', '0x7', '0x7', '0x1', '0x5', '0x1', '0x3', '0x4', '0x4', '0x4', '0x6', '0x7', '0x4', '0x0', '0x2', '0x4', '0x1', '0x4', '0x6', '0x2', '0x1', '0x2', '0x7', '0x7', '0x4', '0x2', '0x0', '0x6', '0x5', '0x4', '0x3', '0x6', '0x2', '0x4', '0x7', '0x3', '0x4', '0x4', '0x1', '0x6', '0x4', '0x3', '0x2', '0x4', '0x0', '0x7', '0x4', '0x5', '0x0', '0x0', '0x3', '0x7', '0x2', '0x5', '0x4', '0x3', '0x7', '0x6', '0x4', '0x2', '0x0', '0x1', '0x5', '0x3', '0x4', '0x3', '0x1', '0x0', '0x1', '0x3', '0x1', '0x5', '0x4', '0x5', '0x7', '0x2', '0x5', '0x0', '0x6', '0x3', '0x0', '0x3', '0x1', '0x1', '0x6', '0x1', '0x1', '0x3', '0x2', '0x3', '0x4', '0x5', '0x6', '0x7', '0x1', '0x5', '0x2', '0x6', '0x3', '0x7', '0x1', '0x4', '0x1', '0x5', '0x6', '0x6', '0x6', '0x0', '0x7', '0x1', '0x5', '0x0', '0x5', '0x4', '0x1', '0x4', '0x2', '0x1', '0x5', '0x0', '0x5', '0x6', '0x0', '0x4', '0x3', '0x0', '0x6', '0x6', '0x5', '0x3', '0x2', '0x5', '0x2', '0x0', '0x4', '0x6', '0x6', '0x7', '0x3', '0x3', '0x4', '0x4', '0x0', '0x0', '0x3', '0x3', '0x5', '0x6', '0x2', '0x5', '0x6', '0x4', '0x6', '0x1', '0x6', '0x7', '0x6', '0x4', '0x3', '0x7', '0x3', '0x7', '0x2', '0x6', '0x5', '0x0', '0x0', '0x4', '0x5', '0x6', '0x5', '0x4', '0x3', '0x1', '0x0', '0x4', '0x3', '0x7', '0x4', '0x0', '0x2', '0x2', '0x6', '0x3', '0x2', '0x4', '0x6', '0x3', '0x3', '0x2', '0x0', '0x4', '0x1', '0x6', '0x0', '0x3', '0x1', '0x5', '0x4', '0x3', '0x3', '0x6', '0x0', '0x3', '0x6', '0x4', '0x7', '0x0', '0x4', '0x1', '0x6', '0x7', '0x1', '0x4', '0x3', '0x1', '0x4', '0x0', '0x4', '0x7', '0x5', '0x7', '0x0', '0x1', '0x4', '0x3', '0x0', '0x7', '0x3', '0x6', '0x7', '0x5', '0x4', '0x3', '0x3', '0x7', '0x7', '0x6', '0x1', '0x4', '0x6', '0x4', '0x4', '0x4', '0x5', '0x6', '0x3', '0x5', '0x6', '0x0', '0x0', '0x3', '0x7', '0x3', '0x7', '0x6', '0x0', '0x7', '0x4', '0x2', '0x1', '0x7', '0x5', '0x0', '0x5', '0x7', '0x1', '0x7', '0x7', '0x0', '0x6', '0x3', '0x1', '0x5', '0x2', '0x5']), header=QobjExperimentHeader(clbit_labels=[['c', 0], ['c', 1], ['c', 2]], creg_sizes=[['c', 3]], global_phase=3.141592653589793, memory_slots=3, metadata={}, n_qubits=5, name='circuit-170', qreg_sizes=[['q', 5]], qubit_labels=[['q', 0], ['q', 1], ['q', 2], ['q', 3], ['q', 4]]), memory=True)], date=2021-10-04 17:02:53-04:00, status=Successful completion, status=QobjHeader(backend_name='ibmq_santiago', backend_version='1.3.31'), time_taken=6.700527906417847, execution_id='6d09d338-2556-11ec-8a7f-b02628eaa3aa', client_version={'qiskit': '0.30.1'})"
      ]
     },
     "execution_count": 49,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "result"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 50,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "{'000': 72,\n",
       " '001': 61,\n",
       " '010': 51,\n",
       " '011': 61,\n",
       " '100': 78,\n",
       " '101': 54,\n",
       " '110': 67,\n",
       " '111': 68}"
      ]
     },
     "execution_count": 50,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "result.get_counts()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 52,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['000',\n",
       " '011',\n",
       " '100',\n",
       " '100',\n",
       " '010',\n",
       " '000',\n",
       " '100',\n",
       " '000',\n",
       " '001',\n",
       " '010',\n",
       " '100',\n",
       " '100',\n",
       " '111',\n",
       " '011',\n",
       " '010',\n",
       " '101',\n",
       " '110',\n",
       " '000',\n",
       " '101',\n",
       " '100',\n",
       " '001',\n",
       " '000',\n",
       " '100',\n",
       " '100',\n",
       " '010',\n",
       " '010',\n",
       " '110',\n",
       " '011',\n",
       " '000',\n",
       " '100',\n",
       " '110',\n",
       " '001',\n",
       " '010',\n",
       " '111',\n",
       " '111',\n",
       " '001',\n",
       " '110',\n",
       " '010',\n",
       " '001',\n",
       " '101',\n",
       " '001',\n",
       " '000',\n",
       " '001',\n",
       " '000',\n",
       " '100',\n",
       " '110',\n",
       " '110',\n",
       " '001',\n",
       " '100',\n",
       " '010',\n",
       " '111',\n",
       " '111',\n",
       " '000',\n",
       " '001',\n",
       " '000',\n",
       " '111',\n",
       " '111',\n",
       " '111',\n",
       " '000',\n",
       " '010',\n",
       " '000',\n",
       " '111',\n",
       " '110',\n",
       " '110',\n",
       " '001',\n",
       " '010',\n",
       " '101',\n",
       " '010',\n",
       " '101',\n",
       " '100',\n",
       " '111',\n",
       " '111',\n",
       " '001',\n",
       " '000',\n",
       " '010',\n",
       " '110',\n",
       " '110',\n",
       " '111',\n",
       " '001',\n",
       " '011',\n",
       " '101',\n",
       " '111',\n",
       " '111',\n",
       " '000',\n",
       " '101',\n",
       " '010',\n",
       " '111',\n",
       " '111',\n",
       " '111',\n",
       " '111',\n",
       " '001',\n",
       " '000',\n",
       " '011',\n",
       " '111',\n",
       " '101',\n",
       " '101',\n",
       " '000',\n",
       " '110',\n",
       " '111',\n",
       " '100',\n",
       " '000',\n",
       " '110',\n",
       " '111',\n",
       " '101',\n",
       " '110',\n",
       " '100',\n",
       " '100',\n",
       " '001',\n",
       " '000',\n",
       " '011',\n",
       " '010',\n",
       " '000',\n",
       " '110',\n",
       " '100',\n",
       " '101',\n",
       " '110',\n",
       " '010',\n",
       " '011',\n",
       " '110',\n",
       " '110',\n",
       " '000',\n",
       " '000',\n",
       " '001',\n",
       " '001',\n",
       " '000',\n",
       " '111',\n",
       " '011',\n",
       " '011',\n",
       " '101',\n",
       " '001',\n",
       " '010',\n",
       " '000',\n",
       " '100',\n",
       " '110',\n",
       " '011',\n",
       " '110',\n",
       " '010',\n",
       " '001',\n",
       " '111',\n",
       " '011',\n",
       " '010',\n",
       " '101',\n",
       " '110',\n",
       " '111',\n",
       " '101',\n",
       " '011',\n",
       " '110',\n",
       " '001',\n",
       " '110',\n",
       " '100',\n",
       " '110',\n",
       " '000',\n",
       " '111',\n",
       " '110',\n",
       " '101',\n",
       " '000',\n",
       " '111',\n",
       " '010',\n",
       " '000',\n",
       " '101',\n",
       " '001',\n",
       " '001',\n",
       " '010',\n",
       " '111',\n",
       " '011',\n",
       " '111',\n",
       " '010',\n",
       " '101',\n",
       " '111',\n",
       " '101',\n",
       " '110',\n",
       " '000',\n",
       " '110',\n",
       " '011',\n",
       " '011',\n",
       " '101',\n",
       " '011',\n",
       " '100',\n",
       " '101',\n",
       " '111',\n",
       " '000',\n",
       " '000',\n",
       " '001',\n",
       " '001',\n",
       " '100',\n",
       " '001',\n",
       " '111',\n",
       " '001',\n",
       " '110',\n",
       " '010',\n",
       " '010',\n",
       " '000',\n",
       " '000',\n",
       " '111',\n",
       " '100',\n",
       " '100',\n",
       " '000',\n",
       " '111',\n",
       " '101',\n",
       " '010',\n",
       " '000',\n",
       " '100',\n",
       " '000',\n",
       " '100',\n",
       " '010',\n",
       " '110',\n",
       " '100',\n",
       " '100',\n",
       " '101',\n",
       " '011',\n",
       " '100',\n",
       " '011',\n",
       " '010',\n",
       " '001',\n",
       " '100',\n",
       " '100',\n",
       " '001',\n",
       " '110',\n",
       " '001',\n",
       " '100',\n",
       " '011',\n",
       " '000',\n",
       " '000',\n",
       " '000',\n",
       " '010',\n",
       " '111',\n",
       " '111',\n",
       " '011',\n",
       " '100',\n",
       " '010',\n",
       " '000',\n",
       " '001',\n",
       " '011',\n",
       " '001',\n",
       " '101',\n",
       " '000',\n",
       " '010',\n",
       " '111',\n",
       " '111',\n",
       " '001',\n",
       " '101',\n",
       " '001',\n",
       " '011',\n",
       " '100',\n",
       " '100',\n",
       " '100',\n",
       " '110',\n",
       " '111',\n",
       " '100',\n",
       " '000',\n",
       " '010',\n",
       " '100',\n",
       " '001',\n",
       " '100',\n",
       " '110',\n",
       " '010',\n",
       " '001',\n",
       " '010',\n",
       " '111',\n",
       " '111',\n",
       " '100',\n",
       " '010',\n",
       " '000',\n",
       " '110',\n",
       " '101',\n",
       " '100',\n",
       " '011',\n",
       " '110',\n",
       " '010',\n",
       " '100',\n",
       " '111',\n",
       " '011',\n",
       " '100',\n",
       " '100',\n",
       " '001',\n",
       " '110',\n",
       " '100',\n",
       " '011',\n",
       " '010',\n",
       " '100',\n",
       " '000',\n",
       " '111',\n",
       " '100',\n",
       " '101',\n",
       " '000',\n",
       " '000',\n",
       " '011',\n",
       " '111',\n",
       " '010',\n",
       " '101',\n",
       " '100',\n",
       " '011',\n",
       " '111',\n",
       " '110',\n",
       " '100',\n",
       " '010',\n",
       " '000',\n",
       " '001',\n",
       " '101',\n",
       " '011',\n",
       " '100',\n",
       " '011',\n",
       " '001',\n",
       " '000',\n",
       " '001',\n",
       " '011',\n",
       " '001',\n",
       " '101',\n",
       " '100',\n",
       " '101',\n",
       " '111',\n",
       " '010',\n",
       " '101',\n",
       " '000',\n",
       " '110',\n",
       " '011',\n",
       " '000',\n",
       " '011',\n",
       " '001',\n",
       " '001',\n",
       " '110',\n",
       " '001',\n",
       " '001',\n",
       " '011',\n",
       " '010',\n",
       " '011',\n",
       " '100',\n",
       " '101',\n",
       " '110',\n",
       " '111',\n",
       " '001',\n",
       " '101',\n",
       " '010',\n",
       " '110',\n",
       " '011',\n",
       " '111',\n",
       " '001',\n",
       " '100',\n",
       " '001',\n",
       " '101',\n",
       " '110',\n",
       " '110',\n",
       " '110',\n",
       " '000',\n",
       " '111',\n",
       " '001',\n",
       " '101',\n",
       " '000',\n",
       " '101',\n",
       " '100',\n",
       " '001',\n",
       " '100',\n",
       " '010',\n",
       " '001',\n",
       " '101',\n",
       " '000',\n",
       " '101',\n",
       " '110',\n",
       " '000',\n",
       " '100',\n",
       " '011',\n",
       " '000',\n",
       " '110',\n",
       " '110',\n",
       " '101',\n",
       " '011',\n",
       " '010',\n",
       " '101',\n",
       " '010',\n",
       " '000',\n",
       " '100',\n",
       " '110',\n",
       " '110',\n",
       " '111',\n",
       " '011',\n",
       " '011',\n",
       " '100',\n",
       " '100',\n",
       " '000',\n",
       " '000',\n",
       " '011',\n",
       " '011',\n",
       " '101',\n",
       " '110',\n",
       " '010',\n",
       " '101',\n",
       " '110',\n",
       " '100',\n",
       " '110',\n",
       " '001',\n",
       " '110',\n",
       " '111',\n",
       " '110',\n",
       " '100',\n",
       " '011',\n",
       " '111',\n",
       " '011',\n",
       " '111',\n",
       " '010',\n",
       " '110',\n",
       " '101',\n",
       " '000',\n",
       " '000',\n",
       " '100',\n",
       " '101',\n",
       " '110',\n",
       " '101',\n",
       " '100',\n",
       " '011',\n",
       " '001',\n",
       " '000',\n",
       " '100',\n",
       " '011',\n",
       " '111',\n",
       " '100',\n",
       " '000',\n",
       " '010',\n",
       " '010',\n",
       " '110',\n",
       " '011',\n",
       " '010',\n",
       " '100',\n",
       " '110',\n",
       " '011',\n",
       " '011',\n",
       " '010',\n",
       " '000',\n",
       " '100',\n",
       " '001',\n",
       " '110',\n",
       " '000',\n",
       " '011',\n",
       " '001',\n",
       " '101',\n",
       " '100',\n",
       " '011',\n",
       " '011',\n",
       " '110',\n",
       " '000',\n",
       " '011',\n",
       " '110',\n",
       " '100',\n",
       " '111',\n",
       " '000',\n",
       " '100',\n",
       " '001',\n",
       " '110',\n",
       " '111',\n",
       " '001',\n",
       " '100',\n",
       " '011',\n",
       " '001',\n",
       " '100',\n",
       " '000',\n",
       " '100',\n",
       " '111',\n",
       " '101',\n",
       " '111',\n",
       " '000',\n",
       " '001',\n",
       " '100',\n",
       " '011',\n",
       " '000',\n",
       " '111',\n",
       " '011',\n",
       " '110',\n",
       " '111',\n",
       " '101',\n",
       " '100',\n",
       " '011',\n",
       " '011',\n",
       " '111',\n",
       " '111',\n",
       " '110',\n",
       " '001',\n",
       " '100',\n",
       " '110',\n",
       " '100',\n",
       " '100',\n",
       " '100',\n",
       " '101',\n",
       " '110',\n",
       " '011',\n",
       " '101',\n",
       " '110',\n",
       " '000',\n",
       " '000',\n",
       " '011',\n",
       " '111',\n",
       " '011',\n",
       " '111',\n",
       " '110',\n",
       " '000',\n",
       " '111',\n",
       " '100',\n",
       " '010',\n",
       " '001',\n",
       " '111',\n",
       " '101',\n",
       " '000',\n",
       " '101',\n",
       " '111',\n",
       " '001',\n",
       " '111',\n",
       " '111',\n",
       " '000',\n",
       " '110',\n",
       " '011',\n",
       " '001',\n",
       " '101',\n",
       " '010',\n",
       " '101']"
      ]
     },
     "execution_count": 52,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "myjson = result.get_memory()\n",
    "myjson"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [],
   "source": [
    "import json\n",
    "with open('data.json', 'w') as outfile:\n",
    "    json.dump(myjson, outfile)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
