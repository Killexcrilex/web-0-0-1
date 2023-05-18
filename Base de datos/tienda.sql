-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 18-05-2023 a las 16:14:28
-- Versión del servidor: 10.4.27-MariaDB
-- Versión de PHP: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `tienda`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `administrador`
--

CREATE TABLE `administrador` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `horario` varchar(50) NOT NULL,
  `usuario` varchar(25) NOT NULL,
  `correo` varchar(50) NOT NULL,
  `contra` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `administrador`
--

INSERT INTO `administrador` (`id`, `nombre`, `horario`, `usuario`, `correo`, `contra`) VALUES
(1, 'Francisco Cardenas', '8 a.m- 9.am', 'Frank', 'frankcardenas@gmail.com', 'Frank');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carrito`
--

CREATE TABLE `carrito` (
  `id` int(11) NOT NULL,
  `Producto` varchar(50) NOT NULL,
  `Precio` int(11) NOT NULL,
  `Cantidad` int(11) NOT NULL,
  `Total` int(11) NOT NULL,
  `Correo` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `edad` int(50) NOT NULL,
  `usuario` varchar(25) NOT NULL,
  `correo` varchar(50) NOT NULL,
  `contra` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id`, `nombre`, `edad`, `usuario`, `correo`, `contra`) VALUES
(1, 'Luis Felipe', 12, 'Luis', 'luisfelipe2134@gmail.com', 'Luis');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `codigo` int(11) NOT NULL,
  `Nombre` varchar(50) NOT NULL,
  `preciodecompra` int(11) NOT NULL,
  `preciodeventa` int(11) NOT NULL,
  `existencia` int(11) NOT NULL,
  `restriccion` int(11) NOT NULL,
  `imagen` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`codigo`, `Nombre`, `preciodecompra`, `preciodeventa`, `existencia`, `restriccion`, `imagen`) VALUES
(1, 'Fresca 600 ml', 18, 20, 1, 1, 'fre.jpeg'),
(2, 'Tonayan 500ml', 12, 30, 18, 18, 'tona.jpeg'),
(3, 'Pasta Colgate', 10, 45, 10, 0, 'col.jpg'),
(4, 'Pepsi 600ml', 10, 18, 24, 0, 'pep.jpeg'),
(5, 'Coca-cola 600ml', 13, 18, 24, 0, 'coca.jpg'),
(6, 'Maruchan de Camaron ', 13, 16, 24, 0, 'mar.jpg'),
(7, 'Fanta 600ml', 13, 18, 24, 0, 'fan.jpg'),
(8, 'Doritos Pizzerola', 15, 16, 15, 0, 'dp.jpeg'),
(10, 'Rufles de queso', 17, 18, 15, 0, 'ruf.jpg'),
(11, 'Sabritas crema y especias', 17, 18, 15, 0, 'sce.jpeg'),
(12, 'Cigarros Alaska', 54, 64, 24, 18, 'alas.jpg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ticket`
--

CREATE TABLE `ticket` (
  `id` int(11) NOT NULL,
  `archivo` varchar(50) NOT NULL,
  `numero` int(11) NOT NULL,
  `caducidad` varchar(50) NOT NULL,
  `estado` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ticket`
--

INSERT INTO `ticket` (`id`, `archivo`, `numero`, `caducidad`, `estado`) VALUES
(1, 'juanis1.pdf', 1, '12-05-2023', 'On');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `trabajador`
--

CREATE TABLE `trabajador` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `horario` varchar(50) NOT NULL,
  `salario` int(11) NOT NULL,
  `usuario` varchar(25) NOT NULL,
  `correo` varchar(50) NOT NULL,
  `contra` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `trabajador`
--

INSERT INTO `trabajador` (`id`, `nombre`, `horario`, `salario`, `usuario`, `correo`, `contra`) VALUES
(1, 'Esteban', '12 a.m - 11 a.m', 20, 'Esteban', 'estebanco@gmail.com', 'Esteban'),
(2, 'Miriam Cardenas', '10 a.m- 12 p.m', 200, 'Miriam', 'miriamcardenas@gmail.com', 'Miriam');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `administrador`
--
ALTER TABLE `administrador`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`codigo`);

--
-- Indices de la tabla `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `trabajador`
--
ALTER TABLE `trabajador`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `administrador`
--
ALTER TABLE `administrador`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `codigo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `ticket`
--
ALTER TABLE `ticket`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `trabajador`
--
ALTER TABLE `trabajador`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
