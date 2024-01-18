import jest from 'jest';

/** @type jest.Config */
const config = {
    verbose: true,
    rootDir: './src/test/typescript/',
    preset: 'ts-jest',
    testEnvironment: 'node'
};

export default config;