-- phpMyAdmin SQL Dump
-- version 4.7.1
-- https://www.phpmyadmin.net/
--
-- Servidor: sql5.freemysqlhosting.net
-- Tiempo de generación: 26-09-2022 a las 17:20:19
-- Versión del servidor: 5.5.62-0ubuntu0.14.04.1
-- Versión de PHP: 7.0.33-0ubuntu0.16.04.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `sql5521784`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `records`
--

CREATE TABLE `records` (
  `userId` int(255) NOT NULL,
  `recordId` int(255) NOT NULL,
  `date` date NOT NULL,
  `superString` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `records`
--

INSERT INTO `records` (`userId`, `recordId`, `date`, `superString`) VALUES
(3, 2, '2022-09-24', 'Shower:pressure=high,time=6;WashingMachine:load=7,times=2;Toilet:times=4;Watering:pressure=medium,time=15'),
(1, 1, '2022-09-23', 'Shower:pressure=medium,time=7;WashingMach:load=5,times=3;Toilet:times=3;Watering:pressure=high,time=10'),
(3, 3, '2022-09-23', 'Shower:pressure=medium,time=7;WashingMachine:load=5,times=3;Toilet:times=3;Watering:pressure=low,time=10'),
(3, 4, '2022-09-22', 'Shower:pressure=high,time=9;WashingMachine:load=5,times=0;Toilet:times=4;Watering:pressure=high,time=5'),
(3, 5, '2022-09-21', 'Shower:pressure=medium,time=0;WashingMachine:load=5,times=0;Toilet:times=5;Watering:pressure=low,time=0'),
(3, 6, '2022-09-20', 'Shower:pressure=low,time=20;WashingMachine:load=7,times=4;Toilet:times=1;Watering:pressure=high,time=10'),
(3, 7, '2022-09-19', 'Shower:pressure=medium,time=10;WashingMachine:load=7,times=5;Toilet:times=3;Watering:pressure=low,time=15'),
(3, 8, '2022-09-18', 'Shower:pressure=medium,time=8;WashingMachine:load=7,times=0;Toilet:times=3;Watering:pressure=low,time=0'),
(3, 9, '2022-09-17', 'Shower:pressure=medium,time=8;WashingMachine:load=7,times=0;Toilet:times=3;Watering:pressure=low,time=0'),
(3, 10, '2022-09-16', 'Shower:pressure=high,time=5;WashingMachine:load=5,times=3;Toilet:times=4;Watering:pressure=high,time=10'),
(3, 11, '2022-09-15', 'Shower:pressure=high,time=5;WashingMachine:load=5,times=3;Toilet:times=4;Watering:pressure=high,time=10'),
(3, 12, '2022-09-14', 'Shower:pressure=medium,time=15;WashingMachine:load=5,times=6;Toilet:times=3;Watering:pressure=high,time=0'),
(3, 13, '2022-09-13', 'Shower:pressure=low,time=10;WashingMachine:load=5,times=0;Toilet:times=4;Watering:pressure=high,time=5'),
(3, 14, '2022-09-12', 'Shower:pressure=medium,time=0;WashingMachine:load=5,times=5;Toilet:times=6;Watering:pressure=high,time=15'),
(6, 15, '2022-09-25', 'Shower:pressure=high,time=0;WashingMachine:load=5,times=0;Toilet:times=1;Watering:pressure=high,time=2'),
(6, 16, '2022-09-25', 'Shower:pressure=high,time=0;WashingMachine:load=5,times=0;Toilet:times=0;Watering:pressure=high,time=0'),
(6, 18, '2022-09-25', 'Shower:pressure=high,time=10;WashingMachine:load=5,times=0;Toilet:times=2;Watering:pressure=medium,time=0'),
(6, 19, '2022-09-25', 'Shower:pressure=medium,time=0;WashingMachine:load=7,times=0;Toilet:times=0;Watering:pressure=high,time=0'),
(3, 20, '2020-09-26', 'Shower:pressure=medium,time=10;WashingMachine:load=5,times=2;Toilet:times=4;Watering:pressure=low,time=15');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `lastName` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `passcode` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `name`, `lastName`, `username`, `passcode`) VALUES
(1, 'Javier', 'Hernandez', 'Chicharito14', 'Ch141.'),
(2, 'Nicolas', 'Trevino', 'NicoTrevino', '0408N.'),
(3, 'Carlos', 'Martinez', 'CarlosMtz', 'Carlos29.'),
(5, 'Oscar', 'Arreola', 'Osc', '12345'),
(6, '2', '2', '2', '2');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
