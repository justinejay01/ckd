<?php

// autoload_real.php @generated by Composer

class ComposerAutoloaderInita175ff806387c5a2651e9da0c1b2d637
{
    private static $loader;

    public static function loadClassLoader($class)
    {
        if ('Composer\Autoload\ClassLoader' === $class) {
            require __DIR__ . '/ClassLoader.php';
        }
    }

    /**
     * @return \Composer\Autoload\ClassLoader
     */
    public static function getLoader()
    {
        if (null !== self::$loader) {
            return self::$loader;
        }

        require __DIR__ . '/platform_check.php';

        spl_autoload_register(array('ComposerAutoloaderInita175ff806387c5a2651e9da0c1b2d637', 'loadClassLoader'), true, true);
        self::$loader = $loader = new \Composer\Autoload\ClassLoader(\dirname(__DIR__));
        spl_autoload_unregister(array('ComposerAutoloaderInita175ff806387c5a2651e9da0c1b2d637', 'loadClassLoader'));

        require __DIR__ . '/autoload_static.php';
        call_user_func(\Composer\Autoload\ComposerStaticInita175ff806387c5a2651e9da0c1b2d637::getInitializer($loader));

        $loader->register(true);

        return $loader;
    }
}
