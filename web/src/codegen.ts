import type { CodegenConfig } from '@graphql-codegen/cli'
 
const config: CodegenConfig = {
   schema: new URL('graphql', import.meta.env.VITE_BACKEND_URL || 'http://localhost:8080').toString(),
   documents: ['src/**/*.svelte'],
   generates: {
      './src/services/http/graphql/stores/': {
        preset: 'client',
      }
   }
}
export default config